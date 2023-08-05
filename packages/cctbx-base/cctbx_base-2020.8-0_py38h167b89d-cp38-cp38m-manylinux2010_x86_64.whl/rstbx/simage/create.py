from __future__ import absolute_import, division, print_function
phil_str = """\
base36_timestamp = None
  .type = str
pdb_id = None
  .type = str
pdb_file = None
  .type = path
reset_b_factors_value = None
  .type = float
change_of_basis_op_to_niggli_cell = None
  .type = str
unit_cell = None
  .type = unit_cell
intensity_symmetry = None
  .type = space_group
lattice_symmetry = None
  .type = space_group
lattice_symmetry_max_delta = 1.4
  .type = float
anomalous_flag = True
  .type = bool
euler_angles_xyz = 0 0 0
  .type = floats(size=3)
crystal_rotation_matrix = None
  .type = floats(size=9)
wavelength = 1
  .type = float
wavelength_2 = None
  .type = float
d_min = 2
  .type = float
ewald_proximity = 0.0025
  .type = float
signal_max = 60000
  .type = int
point_spread = 6
  .type = int
gaussian_falloff_scale = 4
  .type = float
noise {
  max = 10
    .type = int
  random_seed = 0
    .type = int
}
detector {
  distance = None
    .type = float
  size = 200 200
    .type = floats(size=2)
  pixels = 1000 1000
    .type = ints(size=2)
  use_corners = False
    .type = bool
}
force_unit_spot_intensities = False
  .type = bool
"""

def compute_detector_d_min(work_params):
  dsx, dsy = work_params.detector.size
  half_diag = (dsx**2 + dsy**2)**0.5 / 2
  import math
  theta_rad = math.atan2(half_diag, work_params.detector.distance) / 2
  assert theta_rad != 0
  denom = 2 * math.sin(theta_rad)
  assert denom != 0
  return round(work_params.wavelength / denom, 2)

def compute_detector_distance(work_params):
  sin_theta = work_params.wavelength / (2 * work_params.d_min)
  import math
  two_theta_rad = math.asin(sin_theta) * 2
  two_theta = two_theta_rad * 180 / math.pi
  if (two_theta > 89):
    raise RuntimeError(
      "two_theta = %.2f degrees (limit is 89 degrees)" % two_theta)
  tan_two_theta = math.tan(two_theta_rad)
  if (work_params.detector.use_corners):
    dsx, dsy = work_params.detector.size
    half_diag = (dsx**2 + dsy**2)**0.5 / 2
    limit = half_diag
  else:
    half_detector = min(work_params.detector.size) / 2
    limit = half_detector
  return int(limit / tan_two_theta)

def adjust_unit_cell_and_intensity_symmetry(work_params):
  assert work_params.change_of_basis_op_to_niggli_cell is None
  assert work_params.lattice_symmetry is None
  unit_cell = work_params.unit_cell
  intensity_symmetry = work_params.intensity_symmetry
  assert unit_cell is not None
  if (intensity_symmetry is not None):
    intensity_symmetry = intensity_symmetry.group()
    assert intensity_symmetry.is_compatible_unit_cell(unit_cell)
    from cctbx import crystal
    cb_op = crystal.symmetry(
      unit_cell=unit_cell,
      space_group=intensity_symmetry).change_of_basis_op_to_niggli_cell()
  else:
    cb_op = unit_cell.change_of_basis_op_to_niggli_cell()
  unit_cell = unit_cell.change_basis(cb_op)
  if (intensity_symmetry is None):
    g = h = unit_cell.lattice_symmetry_group(
      max_delta=work_params.lattice_symmetry_max_delta)
  else:
    h = intensity_symmetry \
      .change_basis(cb_op) \
      .build_derived_acentric_group() \
      .build_derived_reflection_intensity_group(anomalous_flag=True)
    assert h.is_compatible_unit_cell(unit_cell)
    g = unit_cell.lattice_symmetry_group(
      max_delta=work_params.lattice_symmetry_max_delta)
  assert not g.is_centric()
  assert not h.is_centric()
  work_params.change_of_basis_op_to_niggli_cell = str(cb_op)
  work_params.unit_cell = g.average_unit_cell(unit_cell)
  work_params.intensity_symmetry = h.info()
  work_params.lattice_symmetry = g.info()

def process_args(args, extra_phil_str="", out=None):
  if (out is None):
    import sys
    out = sys.stdout
  import iotbx.phil
  import os
  op = os.path
  master_phil = iotbx.phil.parse(input_string=phil_str+extra_phil_str)
  work_phil = master_phil.command_line_argument_interpreter() \
    .process_and_fetch(args=args)
  work_params = work_phil.extract()
  if (work_params.base36_timestamp is None):
    import libtbx.utils
    work_params.base36_timestamp = libtbx.utils.base36_timestamp()
  if (work_params.pdb_id is None and work_params.pdb_file is None):
    if (work_params.unit_cell is None):
      for cell_sym in [
            work_params.lattice_symmetry,
            work_params.intensity_symmetry]:
        if (cell_sym is None):
          continue
        work_params.unit_cell = cell_sym.primitive_setting() \
          .any_compatible_unit_cell(volume=50**3)
        work_params.lattice_symmetry = None
        break
      else:
        from cctbx import uctbx
        work_params.unit_cell = uctbx.unit_cell((48,58,50,85,95,105))
  else:
    import iotbx.pdb
    pdb_inp = iotbx.pdb.input(
      file_name=work_params.pdb_file,
      pdb_id=work_params.pdb_id)
    assert pdb_inp.source_info().startswith("file ")
    work_params.pdb_file = pdb_inp.source_info()[5:]
    crystal_symmetry = pdb_inp.crystal_symmetry()
    print("Crystal symmetry from PDB file:", file=out)
    crystal_symmetry.show_summary(f=out, prefix="  ")
    print(file=out)
    assert crystal_symmetry.unit_cell() is not None
    assert crystal_symmetry.space_group_info() is not None
    if (work_params.unit_cell is None):
      work_params.unit_cell = crystal_symmetry.unit_cell()
    if (work_params.intensity_symmetry is None):
      work_params.intensity_symmetry = crystal_symmetry.space_group_info()
  adjust_unit_cell_and_intensity_symmetry(work_params)
  if (work_params.d_min is None):
    work_params.d_min = compute_detector_d_min(work_params)
  else:
    work_params.detector.distance = compute_detector_distance(work_params)
  work_phil = master_phil.format(python_object=work_params)
  work_phil.show(out=out)
  print(file=out)
  work_params = work_phil.extract()
  work_params.__inject__("phil_master", work_phil)
  return work_params

def build_i_calc(work_params):
  from scitbx.array_family import flex
  d_min = work_params.d_min
  if (work_params.pdb_file is None):
    miller_set = work_params.unit_cell \
      .complete_miller_set_with_lattice_symmetry(
        d_min=d_min,
        anomalous_flag=True).expand_to_p1()
    if (work_params.intensity_symmetry is not None):
      miller_set = miller_set.customized_copy(
        space_group_info=work_params.intensity_symmetry,
        anomalous_flag=work_params.anomalous_flag).unique_under_symmetry()
    mt = flex.mersenne_twister(seed=work_params.noise.random_seed)
    i_calc_asu = miller_set.array(
      data=mt.random_double(size=miller_set.indices().size()))
  else:
    import iotbx.pdb
    pdb_inp = iotbx.pdb.input(file_name=work_params.pdb_file)
    xs = pdb_inp.xray_structure_simple().change_basis(
      cb_op=work_params.change_of_basis_op_to_niggli_cell)
    assert xs.unit_cell().is_similar_to(other=work_params.unit_cell)
    _ = work_params.reset_b_factors_value
    if (_ is not None):
      from cctbx import adptbx
      u_iso = adptbx.b_as_u(_)
      xs.convert_to_isotropic()
      for sc in xs.scatterers():
        sc.u_iso = u_iso
    miller_set = work_params.unit_cell \
      .complete_miller_set_with_lattice_symmetry(
        d_min=d_min,
        anomalous_flag=work_params.anomalous_flag) \
          .expand_to_p1().customized_copy(
            space_group_info=xs.space_group_info()) \
              .unique_under_symmetry() \
              .remove_systematic_absences() \
              .map_to_asu()
    i_calc_asu = miller_set.structure_factors_from_scatterers(
      xray_structure=xs).f_calc().intensities()
    if (i_calc_asu.data().size() != 0):
      i_calc_max = flex.max(i_calc_asu.data())
      if (i_calc_max > 0):
        i_calc_asu = i_calc_asu.array(data=i_calc_asu.data() * (1/i_calc_max))
    i_calc_asu = i_calc_asu.customized_copy(
      space_group_info=i_calc_asu.space_group()
        .build_derived_reflection_intensity_group(anomalous_flag=True).info()) \
      .map_to_asu() \
      .complete_array(new_data_value=0)
  i_calc_asu = i_calc_asu.sort(by_value="resolution")
  assert not i_calc_asu.space_group().is_centric()
  assert i_calc_asu.space_group().n_ltr() == 1
  assert i_calc_asu.space_group_info().type().is_symmorphic()
  if (work_params.force_unit_spot_intensities):
    i_calc_asu = i_calc_asu.array(
      data=flex.double(i_calc_asu.indices().size(), 1))
  i_asu_array = i_calc_asu.customized_copy(
    data=flex.size_t_range(i_calc_asu.indices().size()))
  if (not i_asu_array.anomalous_flag()):
    i_asu_array = i_asu_array.generate_bijvoet_mates()
  i_asu_array = i_asu_array.expand_to_p1()
  asu_iselection = i_asu_array.data()
  i_calc_p1_anom = i_asu_array.customized_copy(
    data=i_calc_asu.data().select(asu_iselection))
  from libtbx import group_args
  return group_args(
    asu=i_calc_asu,
    asu_iselection=asu_iselection,
    p1_anom=i_calc_p1_anom)

def add_noise(work_params, pixels):
  if (work_params.noise.max > 0):
    from scitbx.array_family import flex
    mt = flex.mersenne_twister(seed=work_params.noise.random_seed)
    noise = mt.random_size_t(
      size=pixels.size(),
      modulus=work_params.noise.max).as_int()
    noise.reshape(pixels.accessor())
    pixels += noise

def compute(
      work_params,
      use_wavelength_2=False,
      store_miller_index_i_seqs=False,
      store_spots=False,
      store_signals=False,
      set_pixels=False):
  i_calc = build_i_calc(work_params)
  from scitbx.math.euler_angles import xyz_matrix
  crystal_rotation_matrix = xyz_matrix(*work_params.euler_angles_xyz)
  work_params.crystal_rotation_matrix = crystal_rotation_matrix
  if (not use_wavelength_2):
    wavelength = work_params.wavelength
  else:
    wavelength = work_params.wavelength_2
  from rstbx.simage import image_simple
  return i_calc, image_simple(
    store_miller_index_i_seqs=store_miller_index_i_seqs,
    store_spots=store_spots,
    store_signals=store_signals,
    set_pixels=set_pixels).compute(
      unit_cell=i_calc.p1_anom.unit_cell(),
      miller_indices=i_calc.p1_anom.indices(),
      spot_intensity_factors=i_calc.p1_anom.data(),
      crystal_rotation_matrix=crystal_rotation_matrix,
      ewald_radius=1/wavelength,
      ewald_proximity=work_params.ewald_proximity,
      signal_max=work_params.signal_max,
      detector_distance=work_params.detector.distance,
      detector_size=work_params.detector.size,
      detector_pixels=work_params.detector.pixels,
      point_spread=work_params.point_spread,
      gaussian_falloff_scale=work_params.gaussian_falloff_scale)

def compute_image(work_params, use_wavelength_2=False):
  _, image_info = compute(
    work_params=work_params,
    use_wavelength_2=use_wavelength_2,
    set_pixels=True)
  pixels = image_info.pixels
  add_noise(work_params, pixels=pixels)
  return pixels
