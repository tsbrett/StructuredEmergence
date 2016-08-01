#! /usr/bin/env python

import numpy as np
import numpy.random

import re
import sys
import os

#eta = 1.0
#gamm = 1.0
##shape parameter for gamma distribution:
#k = 0.2
#Tend = 52*float(sys.argv[1])
#dbeta = 1.2/Tend
#a_no = 4
#s_no = 2
#N = 1000
#dto = 1.0

#zeta = eta/N
#BetaMean = 0.5


class MySimulator:

    def __init__(self):
        self.beta = np.array([[0.1]])
        self.eta = np.array([1])
        self.gamm = np.array([1])
        self.initial_condition = np.array([0])
        self.time_step = 1.
        self.number_time_steps = 100
        
	##Matrix which determines rate at which class i infects class j. N by N
    def secondary_infection(self, state):
	    #r = np.array([beta[i,:]*state[i] for i in range(state)])
	    return((self.beta.T*state).T)
    
    def recovery_vector(self,state):
	    return(self.gamm*state)

    ## Vector determining rate at which class j aquires infection:
    def infection_vector(self,state):
        sec_inf = np.sum(self.secondary_infection(state), axis =0)
        inf_rate = sec_inf + self.eta
        return(inf_rate)
        
    def rates(self, state):
        return(np.concatenate([self.infection_vector(state), self.recovery_vector(state)]))
    
        
    def simulate(self):
    
        N_classes = len(self.initial_condition)
        
        if(np.size(self.eta) != N_classes or np.size(self.gamm) != N_classes or np.size(self.beta,0) != N_classes or np.size(self.beta,1) != N_classes):
            return("t.")
 
 
       	N_reactions = len(self.rates(self.initial_condition))

      	    
       	P = -np.log(np.random.rand(N_reactions))
       	T = np.zeros(N_reactions)
        D = np.zeros(N_reactions)
       	t = 0.
       	te = 0.
       	q = 0
       	n = self.initial_condition
       	n_tot = sum(n)
       	cases = np.zeros(N_classes)
       	cases_tot = sum(cases)
       	
        output = np.empty(shape=[0, N_classes + 2])
        output_cases = np.empty(shape=[0, N_classes + 2])
    
       

       	
        while t >= 0:

	        #Output at equal timesteps:
            if t>=te:
                while(te <= t and q < self.number_time_steps):
                    q = q + 1                    
                    #([te] + n.tolist()), sep = "\t")
                    output = np.append(output, [[te] + n.tolist() + [n_tot]], axis=0)
                    output_cases = np.append(output_cases, [[te] + cases.tolist() + [cases_tot]], axis=0)
                    cases = np.zeros(N_classes)
                    cases_tot = 0
                                      
                    te = te + self.time_step                
                if q == self.number_time_steps:
                    break

			        
            #Updating the reaction rates:      
            a = self.rates(n)



            #Calculating which reaction fires next:
            with np.errstate(divide='ignore'):
            	D = np.divide(P-T,a) #(P - T)/a
	
            dt = float('inf')
            for k in range(N_reactions):
                if a[k] > 10e-20:
                    if D[k] <= dt:
                        dt = D[k] 
                        nu = k
            
            #Updating the internal Possion process and system state according to the reaction which fired:
            t = t+ dt;

		    #Birth:
            if nu < N_classes:
                n[nu] = n[nu] + 1
                cases[nu] = cases[nu] + 1
                cases_tot = cases_tot + 1
                n_tot = n_tot + 1

		    #Death:
            else:
                n[nu-N_classes] = n[nu-N_classes] - 1
                n_tot = n_tot - 1
            
            P[nu] = P[nu] - np.log(np.random.rand())
            #Internal clocks are updated:
            T = T + dt*a
        
        return([output,output_cases])		
