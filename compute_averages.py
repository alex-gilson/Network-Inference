#!/Users/pranavmalhotra/anaconda2/bin/python

import sys
import csv

with open(sys.argv[1], 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	acc=0
	pre=0
	rec=0
	for row in spamreader:
		acc += float(row[3])
		pre += float(row[7])
		rec += float(row[9])

averaged_results=[acc/10, pre/10, rec/10]

with open(sys.argv[2], 'a') as csvfile:
	writer=csv.writer(csvfile,delimiter=',')
	writer.writerow(averaged_results)


