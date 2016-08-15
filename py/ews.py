#! /usr/bin/env python

import sys
import os
import subprocess
import numpy as np
import random as rp
import string
import math
import ews_timeseries_analysis as ts
import pyximport; pyximport.install()
import kolmogorov_complexity as kc
import entropy as entropy
import re
import warnings
from scipy import signal
import pandas as pd

## The future warning being ignored is due to handleing of NaN in sums by numpy.
warnings.simplefilter(action = "ignore", category = FutureWarning)



def get_ews(R0,x, windowsize, ac_timediff ):

	#Mean:
	mu = ts.MovingWindowAverage(x, windowsize)
	#Second Moment:
	mu2 = ts.MovingWindowAverage(x**2, windowsize)
	#Variance:
	var = ts.MovingVariance(x, windowsize)
	#Coefficient of variation:
	Cov = np.sqrt(var)/mu
	#Index of dispersion:
	IoD = var/mu
	#Autocorrelation:
	AC = ts.MovingAC(x,windowsize,ac_timediff)
	#Correlation time:
	CT = -ac_timediff/np.log(abs(AC))
	#Shannon entropy:
	SE = entropy.MovingEntropy(entropy.MovingProb(x, windowsize))
	#Kolmogorov complexity: (not this takes significantly longer to calculate than the other EWS)


	KC = kc.CMovingKC(x,mu, windowsize)

	#Detrending for pej:

	y = signal.detrend(x, type='linear', bp = [len(x)/2])
	m = np.zeros(len(y))
	KC = kc.CMovingKC(y,m, windowsize)

	KC = kc.CMovingKC_detrend(x, windowsize)

	BinTS = kc.binaryTimeseries(x,mu)
	col_names = ["R0", "x", "mean", "var", "cov", "iod", "AC", "CT", "SE", "KC"]
	col_data = [R0, x, mu, var, Cov, IoD, AC, CT, SE, KC] 
	ews_data = dict(zip(col_names,col_data))
	return(ews_data)







