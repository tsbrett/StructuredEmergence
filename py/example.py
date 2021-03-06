#! /usr/bin/env python

import csv_writer
import simulator as sim
import importlib
import numpy as np
import plot_cases

importlib.reload(sim)

#dispersion:
k = 5
#mean infectiousness:
beta = 0.5
#Cut off
n = beta/(beta +1/k)

beta_prob =  [nbinom.pmf(i, n, 1/k) for i in range(N_classes)]
beta_prob = beta_prob/sum(beta_prob)

test = sim.MySimulator()
##Matrix which determines rate at which class i infects class j. N_classes by N_classes
test.beta = np.array([[i*beta_prob[j]   for j in range(N_classes)] for i in range(N_classes)])
test.initial_condition = np.array([1,0,0])
test.gamm = np.array([2.,2.,2.])
test.eta = np.array([1.,0.,0.])
test.time_step = 1.
test.number_time_steps = 100




results = test.simulate()
#n_total = np.transpose([np.sum(results[0],axis=1)-results[0][:,0]])
#results[0] = np.append(results[0], n_total,1)
csv_writer.file_writer("./test.csv", results[0])
csv_writer.file_writer("./test_cases.csv", results[1])

plot_cases.plot_cases("./test_cases.csv","cases.png")
