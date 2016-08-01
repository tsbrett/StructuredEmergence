#! /usr/bin/env python

import csv
import numpy

def file_writer(filename, data):
	with open(filename, 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter = "\t")
		for i in range(len(data)):
			spamwriter.writerow(data[i,:])
