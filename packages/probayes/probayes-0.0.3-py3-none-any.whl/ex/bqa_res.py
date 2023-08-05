import sys
sys.path.append('/mnt/ntfs/g/GSB/code/python/pc/gen/')
import os
import glob
from iofunc import *
from fpfunc import *
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
matplotlib.rc('image', cmap='jet')
from pylab import *; ion()

ipd = "/tmp/bqa/analyses/Q/tdf/s/"
ipe = ".tdf"
xlbl = "Range / probability"
ylbls = [r'$\hat{n}$', r'$\hat{q}$']
ylims = [(0, 20), (0, 200)]
res = 729

_files = glob.glob(ipd + '*' + ipe)
N = len(_files)
labels = np.empty(N, dtype=float)
unsorted = [None] * N
for i in range(N):
  _, filename = os.path.split(_files[i])
  labels[i] = float(filename[1:].replace(ipe, ''))
  unsorted[i] = readDTFile(ipd + filename)[0]

sortind = np.argsort(labels)
vals = labels[sortind]
n_sim = len(unsorted[0])
n_par = len(unsorted[0][0])
data = [np.empty([N, n_sim]) for _ in range(n_par)]

for i in range(N):
  idx = sortind[i]
  for j in range(n_par):
    for k in range(n_sim):
      data[j][i][k] = float(unsorted[idx][k][j])

gck = [None] * n_par
pmf = [None] * n_par
for i in range(n_par):
  gck[i] = gckernel()
  gck[i].setResn(res)
  gck[i].convolve(list(data[i]))
  pmf[i] = gck[i].P

figure()
for i in range(n_par-1):
  subplot(1, n_par-1, i+1)
  quantiles = np.quantile(data[i], [0.025, 0.5, 0.975], axis=1)
  P = pmf[i][:-1, :-1].T
  pcolor(vals, gck[i].x, P)
  plot(vals, quantiles[0], 'w')
  plot(vals, quantiles[1], 'k')
  plot(vals, quantiles[2], 'w')
  xlim(np.min(vals), np.max(vals))
  ylim(ylims[i])
  xlabel(xlbl)
  ylabel(ylbls[i])
