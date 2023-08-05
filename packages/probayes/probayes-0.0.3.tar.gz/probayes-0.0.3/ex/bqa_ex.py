import pyclamp
from pyclamp.dsp.iofunc import *
from pyclamp.qnp.bqa_dgei import BQA
import glob
import datetime
import matplotlib
matplotlib.use("Qt5Agg")
from pylab import *; ion()
from pyclamp.qnp.bqa_dgei import BQA 
ipf = '/tmp/bqa_test.tab'
eps = 10.
nmax = 12

x = list(readDTData(ipf)[0])
self = BQA()
self.set_lims([1, nmax])
self.set_data(x, eps)
self.dgei()
