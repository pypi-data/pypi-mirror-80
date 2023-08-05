import os
import sys
sys.path.append('/mnt/ntfs/g/GSB/code/python/pc/gen/')
import glob
from iofunc import *
import datetime
import matplotlib
matplotlib.use("Qt5Agg")
from pylab import *; ion()
from ex.bqa_dgei import BQA 
ipd = "/tmp/bqa/data/Q/S/"
ipe = ".tab"
opd = "/tmp/bqa/analyses/Q/tdf/s/"
ope = ".tdf"
eps = 20.
nmax = 20
qres = 128
gres = 128
overwrite = False
max_n = None

ipf, ips = lsdir(ipd, ipe, 1)
N = len(ipf)
ops = ips
for i in range(N):
  opf = opd+ops[i]+ope
  if not overwrite and os.path.isfile(opf):
    print("{} skipped".format(opf))
  else:
  #elif ipf[i] == 'S0.05.tab':
    print(datetime.datetime.now().isoformat()+": " + ipf[i])
    X = readDTData(ipd+ipf[i])
    n = len(X)
    hatvals = []
    for j in range(n):
      if max_n is None or j < max_n:
        print(datetime.datetime.now().isoformat()+": " + str(i)+"/"+str(N) + ": " + str(j)+"/"+str(n))
        x = list(X[j])
        self = BQA()
        self.set_lims([1, nmax])
        self.set_data(x, eps)
        self.dgei(1, qres, gres)
        hatval = np.array([self.hatn, self.hatq, self.hatg], dtype=float)
        print(hatval)
        hatvals.append(hatval)
        del self
    hatvals = np.atleast_2d(hatvals)
    writeDTFile(opf, [hatvals])

