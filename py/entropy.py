#! /usr/bin/env python

import numpy as np
#import pandas as pd


   
#Variance in SIS model calculated using VKE:
def VanKampenEntropy(b,g =1, e = 10e-5, N = 1000):
	#Endemic equilibrium for infected individuals:
	p = (b-g-e+np.sqrt((b-g-e)**2+4*b*e))/(2*b) 
	l = (b - 2*b*p - g - e)
	q = b*p*(1-p) + e*(1-p) + g*p 
	return(np.log(N*q/(2*abs(l))))

##Example of usage:
# import matplotlib.pyplot as plt
# x = np.arange(0,2,0.01) 
# y = np.array([e.vvk(x[i]) for i in range(len(x))])
# plt.plot(x,y)



## Returns a 2-d numpy array prob with element prob[i,j] returning the 
## probability of being in state j + min(x) at time t[i]. Assumes timesteps are equal.
## Note: need w >> max(x)-min(x) to have reliable statistics, especially for 
## calculating the entropy
def MovingProb(x, w):
    time = len(x)
    prob = np.zeros((time, max(x)-min(x)+1))
    y = np.array(x) - min(x)
    for i in range(0,(w+1)):
        prob[w,y[i]] = prob[w,y[i]] + 1./w
    for i in range(w+1,time):
        prob[i,:] = prob[i-1,:]
        prob[i,y[i]] = prob[i,y[i]] + 1./w
        prob[i,y[i-w-1]] = prob[i,y[i-w-1]] - 1./w
    return(prob)

## Returns the entropy of the probability distribution as a list.
def MovingEntropy(prob):
    ent = []
    for i in range( prob.shape[0]):
        ent.append( -np.nansum(prob[i,]*np.log(prob[i,])))
    return(ent)
    
def ShannonEntropy(x):
	p, edge = np.histogram(x, bins = max(x)-min(x), density = True)
	return(np.nansum(p*np.log(p)))
