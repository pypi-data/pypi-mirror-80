
"""
Simple Metropolis Hastings sampler taken from Hogg and Foreman-MacKey(2018):

  From Problem 2:
  Sample in a single parameter x and give the sampler 
  as its density function p(x) a Gaussian density with 
  mean 2 and variance 2. Make the proposal distribution 
  q (x'∣x ) a Gaussian pdf for x′ with mean x and 
  variance 1. Initialize the sampler with x = 0 and run 
  the sampler for more than 10000 steps. Plot the results 
  as a histogram with the true density overplotted sensibly.

"""

import prob
import numpy as np
import scipy.stats
import matplotlib
matplotlib.use("Qt5Agg")
from pylab import *; ion()

n_steps = 10000

p = np.empty(n_steps, dtype=float)
x = np.empty(n_steps, dtype=float)
p_last = None
x_last = 0.
for i in range(n_steps):
  dx = scipy.stats.norm.rvs()
  x[i] = x_last + dx
  p[i] = scipy.stats.norm.pdf(x[i], loc=2., scale=np.sqrt(2))
  if i == 0:
    x_last = x[i]
    p_last = p[i]
  else:
    thresh = np.random.uniform()
    if p[i] / p_last >= thresh:
      x_last = x[i]
      p_last = p[i]
    else:
      x[i] = x_last
      p[i] = p_last

xvals = x

figure()
xbins = np.linspace(np.min(xvals), np.max(xvals), 100)
xhist, _ = np.histogram(xvals, xbins)
xprop = xhist / (n_steps * (xbins[1]-xbins[0]))
step(xbins[:-1], xprop, 'b')
norm_x = scipy.stats.norm.pdf(xbins, loc=2, scale=np.sqrt(2)) 
plot(xbins, norm_x, 'r')
    
  

