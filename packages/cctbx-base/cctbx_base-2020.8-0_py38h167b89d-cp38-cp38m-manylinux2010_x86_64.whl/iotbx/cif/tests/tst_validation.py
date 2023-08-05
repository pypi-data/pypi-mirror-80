from __future__ import absolute_import, division, print_function
from iotbx import cif
from iotbx.cif import validation
from iotbx.cif.validation import smart_load_dictionary
import libtbx.load_env
from libtbx.test_utils import Exception_expected

from six.moves.urllib.error import URLError
from six.moves import cStringIO as StringIO
import sys

cif_core_dic_url = "ftp://ftp.iucr.org/pub/cif_core.dic"
cif_mm_dic_url = "ftp://ftp.iucr.org/pub/cif_mm.dic"

def exercise(args):
  import socket
  if socket.getdefaulttimeout() is None:
    socket.setdefaulttimeout(5)
  show_timings = "--show_timings" in args
  exercise_url = "--exercise_url" in args
  try:
    exercise_smart_load(show_timings=show_timings, exercise_url=exercise_url)
  except URLError:
    print("Skipping tst_validation.exercise_smart_load() because of URLError.")
  exercise_dictionary_merging()
  exercise_validation()

def exercise_validation():
  cd = validation.smart_load_dictionary(name="cif_core.dic")
  assert isinstance(cd.deepcopy(), validation.dictionary)
  assert cd.deepcopy() == cd
  assert isinstance(cd.copy(), validation.dictionary)
  assert cd.copy() == cd
  #
  cm_invalid = cif.reader(input_string=cif_invalid).model()
  s = StringIO()
  cm_invalid.validate(cd, out=s)
  assert sorted(cd.err.errors.keys()) == [
    2001, 2002, 2101, 2102, 2501, 2503, 2504, 2505, 2506]
  assert sorted(cd.err.warnings.keys()) == [1001, 1002, 1003]
  cm_valid = cif.reader(input_string=cif_valid).model()
  cd.err.reset()
  s = StringIO()
  cm_valid.validate(cd, out=s)
  assert len(list(cd.err.errors.keys())) == 0
  assert len(list(cd.err.warnings.keys())) == 0
  cd2 = validation.smart_load_dictionary(name="cif_mm.dic")
  cm_invalid_2 = cif.reader(input_string=cif_invalid_2).model()
  s = StringIO()
  cm_invalid_2.validate(cd2, out=s)
  assert sorted(cd2.err.errors.keys()) == [
    2001, 2101, 2102, 2201, 2202, 2203, 2301, 2503, 2504]
  assert cd2.err.error_count == 12
  assert sorted(cd2.err.warnings.keys()) == [1001, 1002]

def exercise_smart_load(show_timings=False, exercise_url=False):
  from libtbx.test_utils import open_tmp_directory
  from libtbx.utils import time_log
  import libtbx
  import os, shutil
  name = ["cif_core.dic", "cif_mm.dic"][0]
  url = [cif_core_dic_url, cif_mm_dic_url][0]
  # from gz
  gz_timer = time_log("from gz").start()
  cd = validation.smart_load_dictionary(name=name)
  gz_timer.stop()
  if exercise_url:
    tempdir = open_tmp_directory()
    store_dir = libtbx.env.under_dist(
      module_name='iotbx', path='cif/dictionaries')
    file_path = os.path.join(store_dir, name) + '.gz'
    shutil.copy(os.path.join(store_dir, name) + '.gz', tempdir)
    # from url
    url_timer = time_log("from url").start()
    cd = validation.smart_load_dictionary(url=url, store_dir=tempdir)
    url_timer.stop()
    # from url to file
    url_to_file_timer = time_log("url to file").start()
    cd = validation.smart_load_dictionary(
      url=url, save_local=True, store_dir=tempdir)
    url_to_file_timer.stop()
    # read local file
    file_timer = time_log("from file").start()
    cd = validation.smart_load_dictionary(file_path=os.path.join(tempdir, name))
    file_timer.stop()
  if show_timings:
    print(time_log.legend)
    print(gz_timer.report())
    if exercise_url:
      print(url_timer.report())
      print(url_to_file_timer.report())
      print(file_timer.report())

def exercise_dictionary_merging():
  #
  # DDL1 merging
  #
  def cif_dic_from_str(string):
    on_this_dict = """
    data_on_this_dictionary
    _dictionary_name dummy
    _dictionary_version 1.0
    """
    return validation.dictionary(
      cif.reader(input_string=on_this_dict+string).model())
  test_cif = cif.reader(input_string="""
  data_test
  _dummy 1234.5
  """).model()
  dict_official = cif_dic_from_str("""
  data_dummy
  _name '_dummy'
  _type numb
  _enumeration_range 0: # i.e. any positive number
  """)
  dict_a = cif_dic_from_str("""
  data_dummy_modified
  _name '_dummy'
  _enumeration_range 0:1000
  """)
  dict_b = cif_dic_from_str("""
  data_dummy
  _name '_dummy'
  _type_extended integer
  """)
  dict_c = cif_dic_from_str("""
  data_dummy
  _name '_dummy'
  _type char
  """)
  test_cif.validate(dict_official)
  try: dict_official.deepcopy().update(other=dict_a, mode="strict")
  except AssertionError: pass
  else: raise Exception_expected
  dict_oa = dict_official.deepcopy()
  dict_oa.update(other=dict_a, mode="overlay")
  assert dict_oa["dummy"]["_type"] == "numb"
  assert dict_oa["dummy"]["_enumeration_range"] == "0:1000"
  assert test_cif.validate(dict_oa, out=StringIO()).error_count == 1
  dict_ao = dict_a.deepcopy()
  dict_ao.update(other=dict_official, mode="overlay")
  assert dict_ao["dummy_modified"]["_type"] == "numb"
  assert dict_ao["dummy_modified"]["_enumeration_range"] == "0:"
  assert test_cif.validate(dict_ao).error_count == 0
  dict_ob = dict_official.deepcopy()
  dict_ob.update(other=dict_b, mode="overlay")
  assert dict_ob["dummy"]["_type"] == "numb"
  assert dict_ob["dummy"]["_type_extended"] == "integer"
  assert test_cif.validate(dict_ob).error_count == 0
  dict_ob = dict_official.deepcopy()
  dict_ob.update(other=dict_b, mode="replace")
  assert "_type" not in dict_ob["dummy"]
  assert dict_ob["dummy"]["_type_extended"] == "integer"
  assert test_cif.validate(dict_ob).error_count == 0
  dict_oc = dict_official.deepcopy()
  dict_oc.update(other=dict_c, mode="replace")
  assert dict_oc["dummy"]["_type"] == "char"
  assert test_cif.validate(dict_oc).error_count == 0
  dict_oc = dict_official.deepcopy()
  dict_oc.update(other=dict_c, mode="overlay")
  errors = test_cif.validate(dict_oc)
  #
  # DDL2 merging
  #
  def cif_dic_from_str(string):
    header = """\
data_test.dic
    _dictionary.title           test.dic
    _dictionary.version         1

    loop_
    _item_type_list.code
    _item_type_list.primitive_code
    _item_type_list.construct
    _item_type_list.detail
               code      char
               '[_,.;:"&<>()/\{}'`~!@#$%A-Za-z0-9*|+-]*'
;              code item types/single words ...
;
"""
    return validation.dictionary(
      cif.reader(input_string=header+string).model())
  dic_a = cif_dic_from_str(
    """
save_fred
    _category.description       'a description'
    _category.id                  fred
    _category.mandatory_code      no
    _category_key.name          'fred.id'
     save_
    """)
  dic_b = cif_dic_from_str(
    """
save_fred
    _category.id                  fred
    _category.mandatory_code      yes
    _category_key.name          'fred.id'
    loop_
    _category_group.id           'inclusive_group'
                                 'atom_group'
     save_
""")
  dic_c = cif_dic_from_str(
    """
save_bob
    _category.id                  bob
    _category.mandatory_code      yes
    _category_key.name          'bob.id'
     save_
""")
  assert dic_a.deepcopy() == dic_a
  assert dic_a.copy() == dic_a
  try: dic_a.deepcopy().update(dic_b, mode="strict")
  except AssertionError: pass
  else: raise Exception_expected
  dic_ab = dic_a.deepcopy()
  dic_ab.update(dic_b, mode="replace")
  assert dic_ab == dic_b
  dic_ab = dic_a.deepcopy()
  dic_ab.update(dic_b, mode="overlay")
  assert dic_ab['test.dic']['fred']['_category.mandatory_code'] == 'yes'
  assert '_category.description' in dic_ab['test.dic']['fred']
  assert '_category_group.id' in dic_ab['test.dic']['fred']
  for mode in ("strict", "replace", "overlay"):
    dic_ac = dic_a.deepcopy()
    dic_ac.update(dic_c, mode=mode)
    assert 'fred' in dic_ac['test.dic']
    assert 'bob' in dic_ac['test.dic']


cif_invalid = """data_1
_made_up_name a                            # warning 1001
_space_group_IT_number b                   # error 2001
_diffrn_reflns_number 2000(1)              # error 2002
_refine_ls_abs_structure_Flack -0.3        # error 2101
_diffrn_radiation_probe rubbish            # error 2102
_symmetry_cell_setting Monoclinic          # warning 1002

loop_
_cell_length_a 10 10                       # error 2501

loop_
_atom_site_label
_atom_site_chemical_conn_number            # error 2504
_atom_site_refinement_flags                # warning 1003
O1 1 P

loop_                                      # error 2503
_atom_site_aniso_label
N1
N2

loop_                                      # error 2505
_space_group_symop_operation_xyz
x,y,z
-x,-y,-z

_atom_site_adp_type Uani                   # error 2506
"""

cif_valid = """data_1
_space_group_IT_number 2
_diffrn_reflns_number 2000
_refine_ls_abs_structure_Flack 0.3
_diffrn_radiation_probe x-ray
_cell_length_a 10
_space_group_crystal_system monoclinic

loop_
_atom_site_label
_atom_site_chemical_conn_number
_atom_site_adp_type
O1 1 Uani
N1 2 Uani
N2 3 Uani

loop_
_chemical_conn_atom_number
_chemical_conn_atom_type_symbol
1 O
2 N
3 N

loop_
_atom_site_aniso_label
N1
N2

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 x,y,z
2 -x,-y,-z
"""

cif_invalid_2 = """data_2
_made_up.name a                            # warning 1001
_space_group.IT_number b                   # error 2001
_diffrn_reflns_number 200.32               # error 2001
_refine.ls_abs_structure_Flack -0.3        # error 2101
_diffrn_radiation.probe rubbish            # error 2102
_symmetry.cell_setting Monoclinic          # warning 1002

loop_
_cell.length_a 10 10                       # error 2203, 2301

loop_
_atom_site.id
_atom_site.chemical_conn_number            # error 2504
O1 1

loop_                                      # error 2503
_atom_site_anisotrop.id
_atom_site_anisotrop.U[1][1]               # error 2301
_atom_site_anisotrop.B[1][1]               # error 2201
_atom_site_anisotrop.U[1][2]_esd           # error 2202
N1 1
N2 2

loop_                                      # error 2203
_space_group_symop.operation_xyz
x,y,z
-x,-y,-z
"""

if __name__ == "__main__":
  exercise(sys.argv[1:])
  print("OK")
