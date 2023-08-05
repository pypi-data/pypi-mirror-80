import pyclamp
from pyclamp.dsp.iofunc import *
import glob
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


ipf, ips = lsdir(ipd, ipe, 1)
N = len(ipf)
ops = ips

for i in range(N):
  X = readDTData(ipd+ipf[i])
  n = len(X)
  n = 1
  for j in range(n):
    x = list(X[j])
    self = BQA()
    self.set_lims([1, nmax])
    self.set_data(x, eps)
    self.dgei()
    break
  break

prob = [None] * 3
for i in range(3):
  logl = self.ll[i].prob
  prob[i] = np.sum(np.exp(logl - logl.max()), axis=1)

vals = self.likelihood.vals
figure()

for i in range(3):
  subplot(2, 3, i+1)
  pcolor(
         np.ravel(vals['q']),
         np.ravel(vals['n']),
         prob[i][:-1, :-1], cmap=cm.jet,
        )
  colorbar()
  xlabel(r'$q$')
  ylabel(r'$n$')
  title(str(i))
  xscale('log')

subplot(2, 3, 5)
pcolor(
       np.ravel(vals['q']),
       np.ravel(vals['n']),
       self.marg_nq.prob[:-1, :-1], cmap=cm.jet,
      )
colorbar()
xlabel(r'$q$')
ylabel(r'$n$')
title(str(i))
xscale('log')
