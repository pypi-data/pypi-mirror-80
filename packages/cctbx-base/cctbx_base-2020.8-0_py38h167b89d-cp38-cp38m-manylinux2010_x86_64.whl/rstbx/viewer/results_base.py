from __future__ import absolute_import, division, print_function

from libtbx import easy_pickle
from libtbx.utils import Sorry
import re
import os
from six.moves import zip

class result(object):
  def __init__(self, dir_name):
    self.dir_name = dir_name
    self._distl = None
    self._labelit = None
    self._groups = None
    distl_file = os.path.join(dir_name, "DISTL_pickle")
    labelit_file = os.path.join(dir_name, "LABELIT_pickle")
    groups_file = os.path.join(dir_name, "LABELIT_possible")
    if (os.path.exists(distl_file)):
      self._distl = easy_pickle.load(distl_file)
    if (os.path.exists(labelit_file)):
      self._labelit = easy_pickle.load(labelit_file)
    if (os.path.exists(groups_file)):
      self._groups = easy_pickle.load(groups_file)

  def get_indexing(self):
    return self._groups

  def get_images(self):
    images = []
    if (self._labelit is not None):
      files = self._labelit['file']
      for id in sorted(files.keys()):
        images.append(files[id])
    return images

  def get_image_id(self, file_name):
    assert (self._labelit is not None)
    files = self._labelit['file']
    for id, fn in files.iteritems():
      if (fn == file_name):
        return id
    return None

  def get_integration_solutions(self):
    solutions = []
    for group in self._groups :
      sol_id = group['counter']
      image_id = sorted(self._labelit['file'].keys())[0]
      integration_file = os.path.join(self.dir_name, "integration_%d_%d.pkl"
        % (sol_id, image_id))
      if (os.path.isfile(integration_file)):
        solutions.append(sol_id)
    return solutions

  def get_integration(self, image_id=1):
    return load_integration_results(self.dir_name, "integration",
      image_id=image_id)

  def get_image_integration(self, sol_id, image_id=None, file_name=None):
    assert (image_id is not None) or (file_name is not None)
    file_name = os.path.join(self.dir_name, "integration_%d_%d.pkl" % (sol_id,
      image_id))
    if (not os.path.exists(file_name)):
      raise Sorry("Can't find the file %s!" % file_name)
    integ_result = easy_pickle.load(file_name)
    summary = get_integration_summary(integ_result, image_id)
    return integ_result, summary

def get_image_id(file_name):
  base, ext = os.path.splitext(file_name)
  fields = base.split("_")
  return int(fields[-1])

def find_integration_files(dir_name, base_name):
  files = []
  for file_name in os.listdir(dir_name):
    if (file_name.startswith(base_name)):
      files.append(os.path.join(dir_name, file_name))
  return files

def get_integration_summary(integ_result, sol_id):
  summary = dict(
    solution=sol_id,
    point_group=integ_result['pointgroup'],
    beam_center=(integ_result['xbeam'], integ_result['ybeam']),
    distance=integ_result['distance'],
    d_min=integ_result['resolution'],
    mosaicity=integ_result['mosaicity'],
    rms=integ_result['residual'],
    bins=integ_result['table_raw'])
  return summary

def load_integration_results(dir_name, base_name, image_id=1):
  files = find_integration_files(dir_name, base_name)
  results = []
  summaries = []
  for file_path in files :
    file_name = os.path.basename(file_path)
    suffix = re.sub(base_name + "_", "", os.path.splitext(file_name)[0])
    sol_id_, img_id_ = suffix.split("_")
    if (int(img_id_) != image_id):
      continue
    print("integration file: %s" % file_path)
    result = easy_pickle.load(file_path)
    results.append(result)
    summary = get_integration_summary(result, int(sol_id_))
    summaries.append(summary)
  r_s = list(zip(results, summaries))
  r_s_sorted = sorted(r_s, key=lambda element: element[1]['solution'], reverse=True)
  return [ r for r,s in r_s_sorted ], [ s for r, s in r_s_sorted ]

class TableData(object):
  """Base class for wx.ListCtrl data source objects in this module."""
  def __init__(self, table):
    assert isinstance(table, list) or isinstance(table, dict)
    self.table = table

  def GetItemCount(self):
    return len(self.table)

  def GetItemImage(self, item):
    return 0

class EmptyData(TableData):
  def __init__(self, *args, **kwds):
    self.table = []

  def GetItemText(self, item, col):
    return ""

class ResultData(TableData):
  def GetItemText(self, item, col):
    n_items = self.GetItemCount()
    assert (item < n_items) and (0 <= col <= 6)
    result = self.table[item]
    if (col == 0):
      return "%d" % result['solution']
    elif (col == 1):
      return result['point_group']
    elif (col == 2):
      return "%.2f %.2f" % result['beam_center']
    elif (col == 3):
      return "%.2f" % result['distance']
    elif (col == 4):
      return "%.2f" % result['d_min']
    elif (col == 5):
      return "%.2f" % result['mosaicity']
    else :
      return "%.3f" % result['rms']

class BinData(TableData):
  def GetItemText(self, item, col):
    n_items = self.GetItemCount()
    assert (item < n_items) and (0 <= col <= 4)
    bin = self.table[item]
    if (col == 0):
      return "%d" % bin.i_bin
    elif (col == 1):
      return "%g - %g" % bin.d_max_min
    elif (col == 2):
      return "%d / %d" % bin.completeness
    elif (col == 3):
      return "%8.1f" % bin.mean_I
    else :
      return "%8.1f" % bin.mean_I_sigI
