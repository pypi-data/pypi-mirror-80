from __future__ import absolute_import, division, print_function
import iotbx.phil
from cctbx.array_family import flex
from libtbx import easy_pickle
from libtbx.utils import Sorry
import sys

den_params = iotbx.phil.parse("""
 reference_file = None
   .type = path
   .optional = true
   .short_caption = DEN reference model
   .style = file_type:pdb input_file
 gamma = 0.5
   .type = float
 kappa = 0.1
   .type = float
 weight = 30.0
   .type = float
 sigma = 0.44
   .type = float
 optimize = True
   .type = bool
   .short_caption = Optimize DEN parameters
   .help = If selected, will run a grid search to determine optimal values \
    of the weight and gamma parameters for DEN refinement.  This is very \
    slow, but highly recommended, and can be parallelized across multiple \
    CPU cores.
 opt_gamma_values = 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
   .type = floats
   .short_caption = Gamma values for optimization
 opt_weight_values = 3.0, 10.0, 30.0, 100.0, 300.0
   .type = floats
   .short_caption = Weight values for optimization
 num_cycles = 10
   .type = int
   .short_caption = Number of cycles
 kappa_burn_in_cycles = 2
   .type = int
   .short_caption = Number of cycles where kappa is set to 0.0
 bulk_solvent_and_scale = True
   .type = bool
   .short_caption = Refine bulk solvent and anisou scale after \
    each DEN cycle
 refine_adp = True
   .type = bool
   .short_caption = Refine B-factors
 final_refinement_cycle = False
   .type = bool
 verbose = False
   .type = bool
 annealing_type = *torsion \
                   cartesian
   .type = choice(multi=False)
   .help = select strategy to apply DEN restraints
 minimize_c_alpha_only = False
   .type = bool
   .short_caption = Restrain only C alpha positions in pre-dynamics \
    coordinate minimization
 output_kinemage = False
   .type = bool
   .help = output kinemage representation of starting DEN restraints
 restraint_network
    .style = box auto_align
 {
  lower_distance_cutoff = 3.0
    .type = float
  upper_distance_cutoff = 15.0
    .type = float
  sequence_separation_low = 0
    .type = int
  sequence_separation_limit = 10
    .type = int
  exclude_hydrogens = True
    .type = bool
  ndistance_ratio = 1.0
    .type = float
  export_den_pairs = False
    .type = bool
    .expert_level = 3
  den_network_file = None
    .type = path
    .optional = True
    .expert_level = 3
 }
""")

den_params_development = iotbx.phil.parse("""
 scale= 150.0
   .type = float
 relax_ncycle = 0
   .type = int
 post_ncycle = 0
   .type = int
 minimum_start = True
   .type = bool
 exponent = *2 4
   .type = choice(multi=False)
 atom_select = None
   .type = atom_selection
   .multiple = True
   .optional = True
""")

class den_restraints(object):

  def __init__(self,
               pdb_hierarchy,
               params,
               pdb_hierarchy_ref=None,
               log=None,
               den_proxies=None):
    if(log is None): log = sys.stdout
    self.log = log
    self.den_proxies = den_proxies
    if len(pdb_hierarchy.models()) > 1:
      raise Sorry("More than one model in input model. DEN refinement "+
                  "is only available for a single model.")
    if pdb_hierarchy_ref is not None:
      if len(pdb_hierarchy_ref.models()) > 1:
        raise Sorry("More than one model in reference model. "+
                    "DEN refinement "+
                    "is only available for a single model.")
    self.pdb_hierarchy = pdb_hierarchy
    atom_labels = list(self.pdb_hierarchy.atoms_with_labels())
    segids = flex.std_string([ a.segid for a in atom_labels ])
    self.use_model_segid = not segids.all_eq('    ')
    if pdb_hierarchy_ref is None:
      print("No input DEN reference model...restraining model "+ \
        "to starting structure", file=self.log)
      self.pdb_hierarchy_ref = pdb_hierarchy
      self.restrain_to_starting_model = True
      self.use_ref_segid = self.use_model_segid
    else:
      self.pdb_hierarchy_ref = pdb_hierarchy_ref
      self.restrain_to_starting_model = False
      ref_atom_labels = \
        list(self.pdb_hierarchy_ref.atoms_with_labels())
      ref_segids = \
        flex.std_string([ a.segid for a in ref_atom_labels ])
      self.use_ref_segid = not ref_segids.all_eq('    ')
    if (not self.use_model_segid) and self.use_ref_segid:
      raise Sorry("Reference model contains SEGIDs that do not match "+\
                  "the working model.")
    elif self.use_model_segid and (not self.use_ref_segid):
      raise Sorry("Working model contains SEGIDs that do not match "+\
                  "the reference model.")
    import boost_adaptbx.boost.python as bp
    self.ext = bp.import_ext("mmtbx_den_restraints_ext")
    self.params = params
    self.kappa = params.kappa
    self.kappa_burn_in_cycles = params.kappa_burn_in_cycles
    self.gamma = params.gamma
    self.weight = params.weight
    self.sigma = params.sigma
    self.num_cycles = params.num_cycles
    self.annealing_type = params.annealing_type
    self.ndistance_ratio = \
      params.restraint_network.ndistance_ratio
    self.lower_distance_cutoff = \
      params.restraint_network.lower_distance_cutoff
    self.upper_distance_cutoff = \
      params.restraint_network.upper_distance_cutoff
    self.sequence_separation_low = \
      params.restraint_network.sequence_separation_low
    self.sequence_separation_limit = \
      params.restraint_network.sequence_separation_limit
    self.exclude_hydrogens = \
      params.restraint_network.exclude_hydrogens
    self.den_network_file = \
      params.restraint_network.den_network_file
    self.export_den_pairs = \
      params.restraint_network.export_den_pairs
    self.current_cycle = None
    self.den_atom_pairs = None
    self.den_pair_count = 0
    self.torsion_mid_point = int(round(self.num_cycles / 2))
    if self.den_proxies is None:
      self.den_proxies = self.ext.shared_den_simple_proxy()

  def build_den_proxies(self, pdb_hierarchy):
    from mmtbx.geometry_restraints.torsion_restraints import utils
    self.atoms_per_chain = \
      self.count_atoms_per_chain(pdb_hierarchy=pdb_hierarchy)
    self.atoms_per_chain_ref = \
      self.count_atoms_per_chain(pdb_hierarchy=self.pdb_hierarchy_ref)
    self.resid_hash_ref = \
      utils.build_resid_hash(pdb_hierarchy=self.pdb_hierarchy_ref)
    self.i_seq_hash = \
      utils.build_i_seq_hash(pdb_hierarchy=pdb_hierarchy)
    self.i_seq_hash_ref = \
      utils.build_i_seq_hash(pdb_hierarchy=self.pdb_hierarchy_ref)
    self.name_hash = \
      utils.build_name_hash(pdb_hierarchy=pdb_hierarchy)
    self.name_hash_ref = \
      utils.build_name_hash(pdb_hierarchy=self.pdb_hierarchy_ref)
    self.ref_atom_pairs, self.ref_distance_hash = \
      self.find_atom_pairs(pdb_hierarchy=self.pdb_hierarchy_ref,
                           resid_hash=self.resid_hash_ref)
    self.remove_non_matching_pairs()
    if self.den_network_file is not None:
      self.den_atom_pairs = self.load_den_network()
    else:
      self.random_ref_atom_pairs = \
        self.select_random_den_restraints()
      self.den_atom_pairs = self.get_den_atom_pairs()
    self.check_den_pair_consistency()
    if self.export_den_pairs:
      self.dump_den_network()

  def check_den_pair_consistency(self):
    if self.den_pair_count == 0:
      raise Sorry("No DEN pairs matched to working model. "+\
                  "Please check inputs.")

  def get_n_proxies(self):
    if self.den_proxies is not None:
      return self.den_proxies.size()
    return 0

  def find_atom_pairs(self, pdb_hierarchy, resid_hash):
    if self.restrain_to_starting_model:
      reference_txt = "starting"
    else:
      reference_txt = "reference"
    print("Finding DEN atom pairs from %s model..." % \
      reference_txt, file=self.log)
    atom_pairs = {}
    distance_hash = {}
    atom_pairs_test = {}
    distance_hash_test = {}
    #only supports first model
    low_dist_sq = self.lower_distance_cutoff**2
    high_dist_sq = self.upper_distance_cutoff**2
    residue_range = \
      self.sequence_separation_limit - self.sequence_separation_low
    for chain in pdb_hierarchy.models()[0].chains():
      found_conformer = chain.conformers()[0]
      if not chain.is_protein() and not chain.is_na():
        continue
      if found_conformer is not None:
        atom_pairs[chain.id] = []
        atom_pairs_test[chain.id] = []
        for i, res1 in enumerate(found_conformer.residues()):
          for res2 in found_conformer.residues()[i:i+residue_range+1]:
            separation = res2.resseq_as_int() - res1.resseq_as_int()
            if separation < self.sequence_separation_low or \
               separation > self.sequence_separation_limit:
              continue
            for j, atom1 in enumerate(res1.atoms()):
              if self.exclude_hydrogens:
                if atom1.element_is_hydrogen():
                  continue
              for atom2 in res2.atoms():
                if atom2.i_seq <= atom1.i_seq:
                  continue
                if self.exclude_hydrogens:
                  if atom2.element_is_hydrogen():
                    continue
                dist = distance_squared(atom1.xyz, atom2.xyz)
                if dist >= low_dist_sq and \
                   dist <= high_dist_sq:
                  atom_pairs[chain.id].append( (atom1.i_seq, atom2.i_seq) )
                  distance_hash[(atom1.i_seq, atom2.i_seq)] = \
                    (dist**(0.5))
    return atom_pairs, distance_hash

  # remove any pairs of reference model atoms that do not
  # have matching atom pairs in the working model
  def remove_non_matching_pairs(self):
    self.den_pair_count = 0
    print("Removing non-matching pairs...", file=self.log)
    temp_atom_pairs = {}
    for chain in self.ref_atom_pairs.keys():
      temp_atom_pairs[chain] = []
      for i, pair in enumerate(self.ref_atom_pairs[chain]):
        ref_atom1 = self.name_hash_ref[pair[0]]
        ref_atom2 = self.name_hash_ref[pair[1]]
        model_atom1 = self.i_seq_hash.get(ref_atom1)
        model_atom2 = self.i_seq_hash.get(ref_atom2)
        if model_atom1 != None and model_atom2 != None:
          temp_atom_pairs[chain].append(pair)
          self.den_pair_count += 1
    self.ref_atom_pairs = temp_atom_pairs
    self.check_den_pair_consistency()

  def count_atoms_per_chain(self, pdb_hierarchy):
    atoms_per_chain = {}
    for chain in pdb_hierarchy.models()[0].chains():
      if not chain.is_protein() and not chain.is_na():
        continue
      if self.exclude_hydrogens:
        counter = 0
        for atom in chain.atoms():
          if not atom.element_is_hydrogen():
            counter += 1
        atoms_per_chain[chain.id] = counter
      else:
        atoms_per_chain[chain.id] = chain.atoms_size()
    return atoms_per_chain

  def select_random_den_restraints(self):
    from cctbx.array_family import flex
    print("Selecting random DEN pairs...", file=self.log)
    random_pairs = {}
    for chain in self.ref_atom_pairs.keys():
      random_pairs[chain] = []
      pair_list_size = len(self.ref_atom_pairs[chain])
      num_restraints = round(self.atoms_per_chain_ref[chain] *
                             self.ndistance_ratio)
      if num_restraints > pair_list_size:
        num_restraints = pair_list_size
      random_selection = \
        flex.random_selection(pair_list_size, int(num_restraints))
      for i in random_selection:
          random_pairs[chain].append(self.ref_atom_pairs[chain][i])
    return random_pairs

  def dump_den_network(self):
    den_dump = {}
    self.get_selection_strings()
    for chain in self.den_atom_pairs.keys():
      den_dump[chain] = []
      for pair in self.den_atom_pairs[chain]:
        i_seq_1 = pair[0]
        i_seq_2 = pair[1]
        select_1 = self.selection_string_hash[i_seq_1]
        select_2 = self.selection_string_hash[i_seq_2]
        dump_pair = (select_1, select_2)
        den_dump[chain].append(dump_pair)
    output_prefix = "den"
    easy_pickle.dump(
      "%s.pkl"%output_prefix,
      den_dump)

  def load_den_network(self):
    self.den_pair_count = 0
    den_atom_pairs = {}
    network_pairs = easy_pickle.load(
      self.den_network_file)
    #check for current model compatibility
    sel_cache = self.pdb_hierarchy.atom_selection_cache()
    for chain in network_pairs.keys():
      den_atom_pairs[chain] = []
      for pair in network_pairs[chain]:
        string = "(%s) or (%s)" % (pair[0], pair[1])
        iselection = sel_cache.selection(string=string).iselection()
        if iselection.size() != 2:
          raise Sorry(
            "input DEN network does not match current model")
        den_atom_pairs[chain].append(iselection)
        self.den_pair_count += 1
    return den_atom_pairs

  def get_selection_strings(self):
    selection_string_hash = {}
    atom_labels = list(self.pdb_hierarchy.atoms_with_labels())
    segids = flex.std_string([ a.segid for a in atom_labels ])
    for a in atom_labels:
      chain = a.chain_id
      resid = a.resid()
      resname = a.resname
      atomname = a.name
      altloc = a.altloc
      segid = a.segid
      selection_string = \
        "name '%s' and resname '%s' and chain '%s' and resid '%s'" % \
        (atomname, resname, chain, resid) + \
        " and segid '%s'" % (segid)
      if altloc != "":
        selection_string += " and altid '%s'" % altloc
      selection_string_hash[a.i_seq] = selection_string
    self.selection_string_hash = selection_string_hash

  def get_den_atom_pairs(self):
    self.den_pair_count = 0
    den_atom_pairs = {}
    for chain in self.random_ref_atom_pairs.keys():
      den_atom_pairs[chain] = []
      for pair in self.random_ref_atom_pairs[chain]:
        i_seq_a = self.i_seq_hash[self.name_hash_ref[pair[0]]]
        i_seq_b = self.i_seq_hash[self.name_hash_ref[pair[1]]]
        i_seqs = flex.size_t([i_seq_a, i_seq_b])
        den_atom_pairs[chain].append(i_seqs)
        self.den_pair_count += 1
    return den_atom_pairs

  def build_den_restraints(self):
    den_weight = self.weight*(1.0/(self.sigma**2))
    print("building DEN restraints...", file=self.log)
    for chain in self.den_atom_pairs.keys():
      for pair in self.den_atom_pairs[chain]:
        i_seq_a = self.i_seq_hash_ref[self.name_hash[pair[0]]]
        i_seq_b = self.i_seq_hash_ref[self.name_hash[pair[1]]]
        distance_ideal = self.ref_distance_hash[ (i_seq_a, i_seq_b) ]
        i_seqs = tuple(pair)
        proxy = self.ext.den_simple_proxy(
          i_seqs=i_seqs,
          eq_distance=distance_ideal,
          eq_distance_start=distance_ideal,
          weight=den_weight)
        self.den_proxies.append(proxy)

  def get_current_eq_distances(self):
    current_eq_distances = []
    for dp in self.den_proxies:
      current_eq_distances.append(dp.eq_distance)
    return current_eq_distances

  def import_eq_distances(self, eq_distances):
    for i, dp in enumerate(self.den_proxies):
      dp.eq_distance = eq_distances[i]

  def target_and_gradients(self,
                           unit_cell,
                           sites_cart,
                           gradient_array):
    return self.ext.den_simple_residual_sum(
      sites_cart,
      self.den_proxies,
      gradient_array,
      self.weight)

  def update_eq_distances(self,
                          sites_cart):
    if self.current_cycle > self.kappa_burn_in_cycles:
      kappa_local = self.kappa
    else:
      kappa_local = 0.0
    self.ext.den_update_eq_distances(sites_cart,
                            self.den_proxies,
                            self.gamma,
                            kappa_local)

  def get_optimization_grid(self):
    # defaults adapted from DEN Nature paper Fig. 1
    gamma_array = self.params.opt_gamma_values
    weight_array = self.params.opt_weight_values
    grid = []
    for g in gamma_array:
      for w in weight_array:
        grid.append( (g, w) )
    return grid

  def show_den_summary(self, sites_cart):
    print("DEN restraints summary:", file=self.log)
    print("\ntotal number of DEN restraints: %s\n" % \
      len(self.den_proxies), file=self.log)
    print("%s | %s | %s | %s | %s " % \
      ("    atom 1     ",
       "    atom 2     ",
       "model dist",
       "  eq dist ",
       "eq dist start"), file=self.log)
    for dp in self.den_proxies:
      i_seqs = dp.i_seqs
      a_xyz = sites_cart[i_seqs[0]]
      b_xyz = sites_cart[i_seqs[1]]
      distance_sq = distance_squared(a_xyz, b_xyz)
      distance = distance_sq**(0.5)
      if self.name_hash[i_seqs[0]].endswith("    "):
        name1 = self.name_hash[i_seqs[0]][:-4]
      else:
        name1 = self.name_hash[i_seqs[0]]
      if self.name_hash[i_seqs[1]].endswith("    "):
        name2 = self.name_hash[i_seqs[1]][:-4]
      else:
        name2 = self.name_hash[i_seqs[1]]
      print("%s | %s |   %6.3f   |   %6.3f   |   %6.3f  " % \
        (name1,
         name2,
         distance,
         dp.eq_distance,
         dp.eq_distance_start), file=self.log)

  def output_kinemage(self, sites_cart):
    from mmtbx.kinemage import validation
    f = open("den_restraints.kin", "w")
    vec_header = "@kinemage\n"
    vec_header += "@vectorlist {DEN} color= magenta master= {DEN}\n"
    f.write(vec_header)
    for dp in self.den_proxies:
      i_seqs = dp.i_seqs
      eq_distance = dp.eq_distance
      site_a = sites_cart[i_seqs[0]]
      site_b = sites_cart[i_seqs[1]]
      sites = [site_a, site_b]
      #distance_sq = distance_squared(site_a, site_b)
      #distance = distance_sq**(0.5)
      #diff = distance - eq_distance
      #spring = validation.add_spring(sites, diff, "DEN")
      vec = validation.kin_vec(start_key="A",
                               start_xyz=site_a,
                               end_key="B",
                               end_xyz=site_b,
                               width=None)
      f.write(vec)
      #STOP()
    #for chain in self.random_ref_atom_pairs.keys():
    #  for pair in self.random_ref_atom_pairs[chain]:
    #    start_xyz = sites_cart[pair[0]]
    #    end_xyz = sites_cart[pair[1]]
    #    vec = validation.kin_vec(start_key="A",
    #                             start_xyz=start_xyz,
    #                             end_key="B",
    #                             end_xyz=end_xyz,
    #                             width=None)
    #   f.write(vec)
    f.close()

  def proxy_select(self, n_seq, selection):
    assert (self.den_proxies is not None)
    return den_restraints(
      pdb_hierarchy=self.pdb_hierarchy,
      params=self.params,
      pdb_hierarchy_ref=self.pdb_hierarchy_ref,
      log=self.log,
      den_proxies=self.den_proxies.proxy_select(n_seq, selection))

def distance_squared(a, b):
  return ((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)
