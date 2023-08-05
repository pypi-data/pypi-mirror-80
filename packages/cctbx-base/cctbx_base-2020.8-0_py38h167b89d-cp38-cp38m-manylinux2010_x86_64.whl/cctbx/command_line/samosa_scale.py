# LIBTBX_SET_DISPATCHER_NAME samosa.scale
from __future__ import absolute_import, division, print_function
import sys

if (__name__ == "__main__"):
  show_plots = False
  if ("--plots" in sys.argv):
    sys.argv.remove("--plots")
    show_plots = True
  from cctbx.examples.merging.samosa.scale import run
  result = run(show_plots=show_plots,args=sys.argv[1:])
  #if result is None:
  #  sys.exit(1)
  #if (show_plots):
  #  result.plots.show_all_pyplot()
  #  from wxtbx.command_line import loggraph
  #  loggraph.run([result.loggraph_file])
