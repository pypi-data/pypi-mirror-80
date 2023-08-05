from __future__ import absolute_import, division, print_function

import sys

import cctbx.masks
from cctbx import maptbx, miller, sgtbx, xray
from cctbx.array_family import flex
from scitbx.math import approx_equal_relatively
from libtbx.utils import xfrange
from six.moves import range


class solvent_accessible_volume(object):
  def __init__(self, xray_structure,
               solvent_radius,
               shrink_truncation_radius,
               ignore_hydrogen_atoms=False,
               crystal_gridding=None,
               grid_step=None,
               d_min=None,
               resolution_factor=1/4,
               atom_radii_table=None,
               use_space_group_symmetry=False):
    self.xray_structure = xray_structure
    if crystal_gridding is None:
      self.crystal_gridding = maptbx.crystal_gridding(
        unit_cell=xray_structure.unit_cell(),
        space_group_info=xray_structure.space_group_info(),
        step=grid_step,
        d_min=d_min,
        resolution_factor=resolution_factor,
        symmetry_flags=sgtbx.search_symmetry_flags(
          use_space_group_symmetry=use_space_group_symmetry))
    else:
      self.crystal_gridding = crystal_gridding
    if use_space_group_symmetry:
      atom_radii = cctbx.masks.vdw_radii(
        xray_structure, table=atom_radii_table).atom_radii
      asu_mappings = xray_structure.asu_mappings(
        buffer_thickness=flex.max(atom_radii)+solvent_radius)
      scatterers_asu_plus_buffer = flex.xray_scatterer()
      frac = xray_structure.unit_cell().fractionalize
      for sc, mappings in zip(
        xray_structure.scatterers(), asu_mappings.mappings()):
        for mapping in mappings:
          scatterers_asu_plus_buffer.append(
            sc.customized_copy(site=frac(mapping.mapped_site())))
      xs = xray.structure(crystal_symmetry=xray_structure,
                          scatterers=scatterers_asu_plus_buffer)
    else:
      xs = xray_structure.expand_to_p1()
    self.vdw_radii = cctbx.masks.vdw_radii(xs, table=atom_radii_table)
    self.mask = cctbx.masks.around_atoms(
      unit_cell=xs.unit_cell(),
      space_group_order_z=xs.space_group().order_z(),
      sites_frac=xs.sites_frac(),
      atom_radii=self.vdw_radii.atom_radii,
      gridding_n_real=self.crystal_gridding.n_real(),
      solvent_radius=solvent_radius,
      shrink_truncation_radius=shrink_truncation_radius)
    if use_space_group_symmetry:
      tags = self.crystal_gridding.tags()
      tags.tags().apply_symmetry_to_mask(self.mask.data)
    self.flood_fill = cctbx.masks.flood_fill(
      self.mask.data, xray_structure.unit_cell())
    self.exclude_void_flags = [False] * self.flood_fill.n_voids()
    self.solvent_accessible_volume = self.n_solvent_grid_points() \
        / self.mask.data.size() * xray_structure.unit_cell().volume()

  def n_voids(self):
    return self.flood_fill.n_voids()

  def n_solvent_grid_points(self):
    return sum([self.mask.data.count(i+2) for i in range(self.n_voids())
                if not self.exclude_void_flags[i]])

  def show_summary(self, log=None):
    if log is None: log = sys.stdout
    print("solvent_radius: %.2f" %(self.mask.solvent_radius), file=log)
    print("shrink_truncation_radius: %.2f" %(
      self.mask.shrink_truncation_radius), file=log)
    print("van der Waals radii:", file=log)
    self.vdw_radii.show(log=log)
    print(file=log)
    print("Total solvent accessible volume / cell = %.1f Ang^3 [%.1f%%]" %(
      self.solvent_accessible_volume,
      100 * self.solvent_accessible_volume /
      self.xray_structure.unit_cell().volume()), file=log)
    n_voids = self.n_voids()
    print(file=log)
    self.flood_fill.show_summary(log=log)




class mask(object):
  def __init__(self, xray_structure, observations, use_set_completion=False):
    self.xray_structure = xray_structure
    self.fo2 = observations.as_intensity_array().average_bijvoet_mates()
    self.use_set_completion = use_set_completion
    if use_set_completion:
      self.complete_set = self.fo2.complete_set()
    else:
      self.complete_set = None
    self.mask = None
    self._f_mask = None
    self.f_000 = None
    self.f_000_s = None
    self.f_000_cell = None
    self._electron_counts_per_void = None

  def compute(self,
              solvent_radius,
              shrink_truncation_radius,
              ignore_hydrogen_atoms=False,
              crystal_gridding=None,
              grid_step=None,
              resolution_factor=1/4,
              atom_radii_table=None,
              use_space_group_symmetry=False):
    if grid_step is not None: d_min = None
    else: d_min = self.fo2.d_min()
    result = solvent_accessible_volume(
      self.xray_structure,
      solvent_radius,
      shrink_truncation_radius,
      ignore_hydrogen_atoms=ignore_hydrogen_atoms,
      crystal_gridding=crystal_gridding,
      grid_step=grid_step,
      d_min=d_min,
      resolution_factor=resolution_factor,
      atom_radii_table=atom_radii_table,
      use_space_group_symmetry=use_space_group_symmetry)
    self.crystal_gridding = result.crystal_gridding
    self.vdw_radii = result.vdw_radii
    self.mask = result.mask
    self.flood_fill = result.flood_fill
    self.exclude_void_flags = [False] * self.flood_fill.n_voids()
    self.solvent_accessible_volume = self.n_solvent_grid_points() \
        / self.mask.data.size() * self.xray_structure.unit_cell().volume()

  def structure_factors(self, max_cycles=10):
    """P. van der Sluis and A. L. Spek, Acta Cryst. (1990). A46, 194-201."""
    assert self.mask is not None
    if self.n_voids() == 0: return
    if self.use_set_completion:
      f_calc_set = self.complete_set
    else:
      f_calc_set = self.fo2.set()
    self.f_calc = f_calc_set.structure_factors_from_scatterers(
      self.xray_structure, algorithm="direct").f_calc()
    f_obs = self.f_obs()
    self.scale_factor = flex.sum(f_obs.data())/flex.sum(
      flex.abs(self.f_calc.data()))
    f_obs_minus_f_calc = f_obs.f_obs_minus_f_calc(
      1/self.scale_factor, self.f_calc)
    self.fft_scale = self.xray_structure.unit_cell().volume()\
        / self.crystal_gridding.n_grid_points()
    epsilon_for_min_residual = 2
    for i in range(max_cycles):
      self.diff_map = miller.fft_map(self.crystal_gridding, f_obs_minus_f_calc)
      self.diff_map.apply_volume_scaling()
      stats = self.diff_map.statistics()
      masked_diff_map = self.diff_map.real_map_unpadded().set_selected(
        self.mask.data.as_double() == 0, 0)
      n_solvent_grid_points = self.n_solvent_grid_points()
      for j in range(self.n_voids()):
        # exclude voids with negative electron counts from the masked map
        # set the electron density in those areas to be zero
        selection = self.mask.data == j+2
        if self.exclude_void_flags[j]:
          masked_diff_map.set_selected(selection, 0)
          continue
        diff_map_ = masked_diff_map.deep_copy().set_selected(~selection, 0)
        f_000 = flex.sum(diff_map_) * self.fft_scale
        f_000_s = f_000 * (
          self.crystal_gridding.n_grid_points() /
          (self.crystal_gridding.n_grid_points() - n_solvent_grid_points))
        if f_000_s < 0:
          masked_diff_map.set_selected(selection, 0)
          f_000_s = 0
          self.exclude_void_flags[j] = True
      self.f_000 = flex.sum(masked_diff_map) * self.fft_scale
      f_000_s = self.f_000 * (masked_diff_map.size() /
        (masked_diff_map.size() - self.n_solvent_grid_points()))
      if (self.f_000_s is not None and
          approx_equal_relatively(self.f_000_s, f_000_s, 0.0001)):
        break # we have reached convergence
      else:
        self.f_000_s = f_000_s
      masked_diff_map.add_selected(
        self.mask.data.as_double() > 0,
        self.f_000_s/self.xray_structure.unit_cell().volume())
      if 0:
        from crys3d import wx_map_viewer
        wx_map_viewer.display(
          title="masked diff_map",
          raw_map=masked_diff_map.as_double(),
          unit_cell=f_obs.unit_cell())
      self._f_mask = f_obs.structure_factors_from_map(map=masked_diff_map)
      self._f_mask *= self.fft_scale
      scales = []
      residuals = []
      min_residual = 1000
      for epsilon in xfrange(epsilon_for_min_residual, 0.9, -0.2):
        f_model_ = self.f_model(epsilon=epsilon)
        scale = flex.sum(f_obs.data())/flex.sum(flex.abs(f_model_.data()))
        residual = flex.sum(flex.abs(
          1/scale * flex.abs(f_obs.data())- flex.abs(f_model_.data()))) \
                 / flex.sum(1/scale * flex.abs(f_obs.data()))
        scales.append(scale)
        residuals.append(residual)
        min_residual = min(min_residual, residual)
        if min_residual == residual:
          scale_for_min_residual = scale
          epsilon_for_min_residual = epsilon
      self.scale_factor = scale_for_min_residual
      f_model = self.f_model(epsilon=epsilon_for_min_residual)
      f_obs = self.f_obs()
      f_obs_minus_f_calc = f_obs.phase_transfer(f_model).f_obs_minus_f_calc(
        1/self.scale_factor, self.f_calc)
    return self._f_mask

  def f_obs(self):
    fo2 = self.fo2.as_intensity_array()
    f_obs = fo2.as_amplitude_array()
    if self.use_set_completion:
      if self._f_mask is not None:
        f_model = self.f_model()
      else:
        f_model = self.f_calc
      data_substitute = flex.abs(f_model.data())
      scale_factor = flex.sum(f_obs.data())/flex.sum(
        f_model.common_set(f_obs).as_amplitude_array().data())
      f_obs = f_obs.matching_set(
        other=self.complete_set,
        data_substitute=scale_factor*flex.abs(f_model.data()),
        sigmas_substitute=0)
    return f_obs

  def f_mask(self):
    return self._f_mask

  def f_model(self, f_calc=None, epsilon=None):
    if self._f_mask is None: return None
    f_mask = self.f_mask()
    if f_calc is None:
      f_calc = self.f_calc
    if epsilon is None:
      data = f_calc.data() + f_mask.data()
    else:
      data = f_calc.data() + epsilon * f_mask.data()
    return miller.array(miller_set=f_calc, data=data)

  def modified_intensities(self):
    """Intensities with the solvent contribution removed."""
    if self._f_mask is None: return None
    f_mask = self.f_mask().common_set(self.fo2)
    f_model = self.f_model().common_set(self.fo2)
    return modified_intensities(
      self.fo2, f_model, f_mask)

  def n_voids(self):
    return self.flood_fill.n_voids()

  def n_solvent_grid_points(self):
    return sum([self.mask.data.count(i+2) for i in range(self.n_voids())
                if not self.exclude_void_flags[i]])

  def electron_counts_per_void(self):
    if self._electron_counts_per_void is not None:
      return self._electron_counts_per_void
    self._electron_counts_per_void = []
    masked_diff_map = self.diff_map.real_map_unpadded().set_selected(
      self.mask.data.as_double() == 0, 0)
    for i in range(self.n_voids()):
      if self.exclude_void_flags[i]:
        f_000_s = 0
      else:
        diff_map = masked_diff_map.deep_copy().set_selected(
          self.mask.data != i+2, 0)
        f_000 = flex.sum(diff_map) * self.fft_scale
        f_000_s = f_000 * (
          self.crystal_gridding.n_grid_points() /
          (self.crystal_gridding.n_grid_points() - self.n_solvent_grid_points()))
      self._electron_counts_per_void.append(f_000_s)
    return self._electron_counts_per_void

  def show_summary(self, log=None):
    if log is None: log = sys.stdout
    print("use_set_completion: %s" %self.use_set_completion, file=log)
    print("solvent_radius: %.2f" %(self.mask.solvent_radius), file=log)
    print("shrink_truncation_radius: %.2f" %(
      self.mask.shrink_truncation_radius), file=log)
    print("van der Waals radii:", file=log)
    self.vdw_radii.show(log=log)
    print(file=log)
    print("Total solvent accessible volume / cell = %.1f Ang^3 [%.1f%%]" %(
      self.solvent_accessible_volume,
      100 * self.solvent_accessible_volume /
      self.xray_structure.unit_cell().volume()), file=log)
    n_voids = self.n_voids()
    if n_voids > 0:
      print("Total electron count / cell = %.1f" %(self.f_000_s), file=log)
    print(file=log)
    self.flood_fill.show_summary(log=log)
    if n_voids == 0: return
    print(file=log)
    print("Void  Vol/Ang^3  #Electrons", file=log)
    grid_points_per_void = self.flood_fill.grid_points_per_void()
    com = self.flood_fill.centres_of_mass_frac()
    electron_counts = self.electron_counts_per_void()
    for i in range(self.n_voids()):
      void_vol = (
        self.xray_structure.unit_cell().volume() * grid_points_per_void[i]) \
               / self.crystal_gridding.n_grid_points()
      formatted_site = ["%6.3f" % x for x in com[i]]
      print("%4i" %(i+1), end=' ', file=log)
      print("%10.1f     " %void_vol, end=' ', file=log)
      print("%7.1f" %electron_counts[i], file=log)

  def as_cif_block(self):
    from iotbx import cif
    cif_block = cif.model.block()
    mask_loop = cif.model.loop(header=(
      "_smtbx_masks_void_nr",
      "_smtbx_masks_void_average_x",
      "_smtbx_masks_void_average_y",
      "_smtbx_masks_void_average_z",
      "_smtbx_masks_void_volume",
      "_smtbx_masks_void_count_electrons",
      "_smtbx_masks_void_content",
    ))
    n_voids = self.n_voids()
    if n_voids == 0: return cif_block
    grid_points_per_void = self.flood_fill.grid_points_per_void()
    com = self.flood_fill.centres_of_mass_frac()
    electron_counts = self.electron_counts_per_void()
    for i in range(self.n_voids()):
      void_vol = (
        self.xray_structure.unit_cell().volume() * grid_points_per_void[i]) \
               / self.crystal_gridding.n_grid_points()
      xyz = list(com[i])
      for j in range(3):
        if round(xyz[j],6) == 0: xyz[j] = 0
      site_fmt = "%.3f"
      mask_loop.add_row(
        [i+1, site_fmt % xyz[0], site_fmt % xyz[1],
         site_fmt % xyz[2], "%.1f" % void_vol,
         "%.1f" %electron_counts[i], '?'])
    cif_block.add_loop(mask_loop)
    cif_block['_smtbx_masks_special_details'] = '?'
    return cif_block


def modified_intensities(observations, f_model, f_mask):
  """Subtracts the solvent contribution from the observed structure
  factors to obtain modified structure factors, suitable for refinement
  with other refinement programs such as ShelXL"""
  f_obs = observations.as_amplitude_array()
  if f_obs.sigmas() is not None:
    weights = weights=1/flex.pow2(f_obs.sigmas())
  else:
    weights = None
  scale_factor = f_obs.scale_factor(f_model, weights=weights)
  f_obs = f_obs.phase_transfer(phase_source=f_model)
  modified_f_obs = miller.array(
    miller_set=f_obs,
    data=(f_obs.data() - f_mask.data()*scale_factor))
  if observations.is_xray_intensity_array():
    # it is better to use the original sigmas for intensity if possible
    return modified_f_obs.as_intensity_array().customized_copy(
      sigmas=observations.sigmas())
  else:
    return modified_f_obs.customized_copy(
      sigmas=f_obs.sigmas()).as_intensity_array()
