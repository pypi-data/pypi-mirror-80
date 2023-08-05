from __future__ import absolute_import, division, print_function
from libtbx import test_utils
import libtbx.load_env

tst_list = [
"$D/tst_cma_es.py",
]

def run():
  build_dir = libtbx.env.under_build("cma_es")
  dist_dir = libtbx.env.dist_path("cma_es")

  test_utils.run_tests(build_dir, dist_dir, tst_list)

if (__name__ == "__main__"):
  run()
