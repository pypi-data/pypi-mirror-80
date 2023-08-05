from __future__ import absolute_import, division, print_function
from mmtbx.tls import tools
import time
from six.moves import range

pdb_str_1 = """
CRYST1   10.000   10.000   10.000  90.00  90.00  90.00 P1
ATOM      1  CA  THR A   6       0.000   0.000   0.000  1.00  0.00           C
ATOM      1  CA  THR B   6       3.000   0.000   0.000  1.00  0.00           C
"""

pdb_str_2 = """
CRYST1   10.000   10.000   10.000  90.00  90.00  90.00 P1
ATOM      1  CA  THR A   6       0.000   0.000   0.000  1.00  0.00           C
ATOM      1  CA  THR B   6       0.000   3.000   0.000  1.00  0.00           C
"""

pdb_str_3 = """
CRYST1   10.000   10.000   10.000  90.00  90.00  90.00 P1
ATOM      1  CA  THR A   6       0.000   0.000   0.000  1.00  0.00           C
ATOM      1  CA  THR B   6       0.000   0.000   3.000  1.00  0.00           C
"""

pdb_str_4 = """
CRYST1   10.000   10.000   10.000  90.00  90.00  90.00 P1
ATOM      1  CA  THR A   6       0.000   0.000   0.000  1.00  0.00           C
ATOM      1  CA  THR B   6       1.000   2.000   3.000  1.00  0.00           C
"""

def exercise_00():
  xs=[0,0,0]
  ys=[0,0,0]
  zs=[0,0,0]
  for pdb_str in [pdb_str_1, pdb_str_2, pdb_str_3, pdb_str_4]:
    print(pdb_str)
    for d in [[0.05,0.06,0.07], ]:
      dx,dy,dz = d
      for x in range(3):
        for y in range(3):
          for z in range(3):
            if(x!=y and x!=z and y!=z):
              xs_ = xs[:]
              ys_ = ys[:]
              zs_ = zs[:]
              xs_[x]=1
              ys_[y]=1
              zs_[z]=1
              tools.u_tls_vs_u_ens(pdb_str=pdb_str,
                dx=dx,dy=dy,dz=dz, sx=0.5,sy=0.4,sz=0.3, lx=xs_,ly=ys_,lz=zs_)
              print()

if (__name__ == "__main__"):
  t0 = time.time()
  exercise_00()
  print("Time: %6.4f"%(time.time()-t0))
  print("OK")
