#! /usr/bin/env python

import numpy as np
import numpy.random

import re
import sys
import os

eta = 1.0
gamm = 1.0
#shape parameter for gamma distribution:
k = 0.2
Tend = 52*float(sys.argv[1])
dbeta = 1.2/Tend
a_no = 4
s_no = 2
N = 1000
dto = 1.0

zeta = eta/N
BetaMean = 0.5


class MySimulator:

    def __init__(self, parameters):
        self.beta = np.array([])
        self.eta = np.array([])
        self.gamm = np.array([])
        self.initial_condition = np.array([])
        
	##Matrix which determines rate at which class i infects class j. N by N
    def secondary_infection(self, state):
	    #r = np.array([beta[i,:]*state[i] for i in range(state)])
	    return((self.beta.T*state).T)
    
    def recovery_vector(self,state):
	    return(self.gamm*state)

    ## Vector determining rate at which class j aquires infection:
    def infection_vector(self,state):
        sec_inf = np.sum(secondary_infection(state), axis =1)
        inf_rate = sec_inf + eta
        return(inf_rate)
        
    def rates(self, state):
    return(np.concatenate(infection_vector(state), recovery_vector(state)))
    
        
    def simulate(self):
        self.N_classes = len(initial_condition)
        if(len(self.eta) != self.N_classes || len(self.gamm) != self.N_classes || len(self.beta[0,:]) != self.N_classes || len(self.beta[:,0]) != self.N_classes):
            return("error")
        else: 
            return("ok")
    
        





#Seed RNG (I think! Also there are faster methods involving drawing less random numbers)
np.random.seed() 

	
def NextImmigrationTime(rate):
	return(np.random.exponential(1.0/rate))
	
def InfectiousnessDistribution(b):
	#gamma distribution: shape and scale
	return(np.random.gamma(k,b/k))
	#return(m)

#more efficient to sort or use dict
def NextRecovery(arr):
	return(np.amin(arr), np.argmin(arr))

def NextInfectionTime(ti):
	return(np.random.exponential(1.0/ti))
	
def RecoveryTime(ip):
	return(np.random.exponential(1.0/ip))
	

beta = []
T_rec_array = []
T_inf_array = []
T_imm = NextImmigrationTime(eta)
T_rec =float('inf')
T_inf =float('inf')
RecReact = 0
n = 0

TotInf = 0.0
t = 0.000001
t_out = 0.0


while(t < Tend):

	Times = [T_inf,T_imm,T_rec]
	NextReaction = np.argmin(Times)
	ReactionTime = Times[NextReaction]
	t = ReactionTime

	#Infection of secondary case:
	if(NextReaction == 0):
		NewInf = InfectiousnessDistribution(dbeta*t)
		beta.append(NewInf)
		TotInf = TotInf + NewInf
		T_inf_array.append(t)
		T_rec_array.append(t+ RecoveryTime(gamm))
		n = n+1

	#Immigration of new infectious individual:
	if(NextReaction ==1):		
		NewInf = InfectiousnessDistribution(dbeta*t)
		beta.append(NewInf)
		TotInf = TotInf + NewInf
		T_inf_array.append(t)
		T_rec_array.append(t+ RecoveryTime(gamm))
		T_imm = t + NextImmigrationTime(eta)
		n = n+1
	
	#Recovery of infectious individual:
	if(NextReaction == 2):
		TotInf = TotInf - beta[RecReact]
		del beta[RecReact]
		del T_rec_array[RecReact]
		del T_inf_array[RecReact]
		n = n -1


	if(n >0):
		T_rec, RecReact = NextRecovery(T_rec_array)
		T_inf = t + NextInfectionTime(TotInf) 	
	else:
		T_rec =float('inf')
		T_inf =float('inf')

	print dbeta*t, t_out, n, dbeta*t
	sys.stdout.flush()			
		
	while(t_out <= t):
		print dbeta*t, t_out, n, dbeta*t
		sys.stdout.flush()	
		t_out = t_out + dto
	
	if(dbeta*t > 1.0): break
				








