from __future__ import absolute_import, division, print_function
import os, sys
import libtbx.load_env
from libtbx import easy_run
from libtbx.test_utils import open_tmp_file, open_tmp_directory

def run(args):
  tmp_dir = open_tmp_directory(suffix="example_cif_parser")
  cur_dir = os.path.abspath(os.path.curdir)
  os.chdir(os.path.abspath(tmp_dir))
  try:
    exercise_compilation()
  finally:
    os.chdir(cur_dir)

def exercise_compilation():
  ucif_dist = libtbx.env.dist_path(module_name="ucif")
  antlr3_dist = libtbx.env.under_dist("ucif", "antlr3")
  os.environ["LIBTBX_UCIF"] = ucif_dist
  os.environ["LIBTBX_ANTLR3"] = antlr3_dist
  assert ucif_dist.find('"') < 0
  if sys.platform == "win32":
    cmd = '"%s/examples/build_cif_parser.bat"' %ucif_dist
    ext = ".exe"
  else:
    cmd = '"%s/examples/build_cif_parser.sh"' %ucif_dist
    ext = ""
  result = easy_run.fully_buffered(cmd)
  if result.return_code:
    if len(result.stderr_lines) > 0:
      raise RuntimeError(result.show_stderr())
    raise RuntimeError(result.show_stdout())
  assert os.path.exists("cif_parser"+ext)
  f = open_tmp_file(suffix=".cif")
  f.write(cif_string)
  f.close()
  cmd = 'cif_parser "%s"' %f.name
  cmd = os.path.join(".", cmd)
  r = easy_run.fully_buffered(cmd).raise_if_errors()
  assert r.stdout_lines[0].startswith("Congratulations!")

cif_string = """\
data_a
_a 1
_b 2
"""

if __name__ == '__main__':
  run(sys.argv[1:])
  print("OK")
