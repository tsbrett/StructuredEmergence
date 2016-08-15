#! /usr/bin/env python

import sys
import os
import subprocess
import numpy as np
import random as rp
import string
import math




def MovingWindowAverage(data, window): #This returns the sum of the datapoints, and does not take into account the stepsize.
	datasum = 0.0
	dataavg = np.zeros(len(data))
	for i in range(window):
		if math.isnan(data[i]) == 0:	 datasum = datasum + data[i]
		dataavg[i] = float('NaN')
	dataavg[window] = datasum/(window)
	for i in range(window, len(data)):
			if math.isnan(data[i])== 0:	 datasum = datasum + data[i] 
			if math.isnan(data[i-window]) == 0:	datasum = datasum - data[i-window]
			dataavg[i] = datasum/(window)
	return(dataavg)


def MovingVariance(data, window):
	mu1 = MovingWindowAverage(data, window)
	mu2 = MovingWindowAverage(data**2, window)
	return(mu2 - mu1**2) 

def MovingAC(data,window,lag):
	
	y = np.concatenate([np.zeros(lag), data[:-lag]])
	cfunc = MovingWindowAverage(data*y,window)
	mu1 = MovingWindowAverage(data,window)
	mu2 = MovingWindowAverage(data**2, window)
	var = mu2 - mu1**2
	mu_y = np.concatenate([np.zeros(lag), mu1[:-lag]])
	var_y = np.concatenate([np.zeros(lag), mu2[:-lag]]) - mu_y**2
	AC = (cfunc - mu1*mu_y)/np.sqrt(var*var_y)
	return(AC)


##############################################################################

### Are these functions even called anywhere?

def extract_systemsize( filename):
	f = open(filename, 'r')
	m = re.search('(?<=N\s=\s)\w+', f.read() )
	f.close()
	systemsize = int(m.group(0))
	return(systemsize)
	
def Fluctuations( pop_size, mean, systemsize): #note that this function takes the mean number of individals as its argument, not the mean concentration
	return( (pop_size - mean)/np.sqrt(systemsize))	

def reactions_update(a,x, vaccine_uptake):
	#Infection:	
	a[0] = beta*x[0]*x[1] + eta*x[0];
	#Recovery or death:
	a[1] = (gamm + mu)*x[1];
	#Birth:
	a[2] = mu*(1-vaccine_uptake);
	#Death of susceptible:
	a[3] = mu*x[0];	

def PowerSpectrum( data, timestep, timeperiod):
	A = np.fft.rfft(data)
	c = timestep**2/timeperiod
	power_spectrum = c*np.abs(A)**2
	return(power_spectrum)

#def Variance(data):
#	return(data**2)

def AutoCorrelation(data, lag): #The output of this function is nonsense for i < lag. Note that if len(data) < lag then all the output is nonsense!
	ac1 = data*np.roll(data,lag)
	for i in range(0, lag): ac1 = float('NaN')
	return(ac1)




