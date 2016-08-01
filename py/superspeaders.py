#! /usr/bin/env python

import csv_writer
import simulator as sim
import importlib
import numpy as np
import plot_cases
from scipy.stats import nbinom

importlib.reload(sim)
#Number of classes:
N_classes = 20
#dispersion:
k = 5.
#mean infectiousness:
beta = 5.0
#mean of nb distribution:
m= 10.
#Cut off
n = m/(m +1/k)

beta_prob =  [nbinom.pmf(i, n, 1/k) for i in range(N_classes)]
beta_prob = beta_prob/sum(beta_prob)

test = sim.MySimulator()
##Matrix which determines rate at which class i infects class j. N_classes by N_classes
test.beta = np.array([[beta*(i/m)*beta_prob[j]   for j in range(N_classes)] for i in range(N_classes)])
test.initial_condition = np.array([1] + [0 for i in range(N_classes-1)])
test.gamm = 2.0*np.ones(N_classes)
test.eta = 1.0*np.array(beta_prob)
test.time_step = 1.
test.number_time_steps = 100




results = test.simulate()
#n_total = np.transpose([np.sum(results[0],axis=1)-results[0][:,0]])
#results[0] = np.append(results[0], n_total,1)
csv_writer.file_writer("./test.csv", results[0])
csv_writer.file_writer("./test_cases.csv", results[1])

plot_cases.plot_cases("./test.csv","cases.png")
