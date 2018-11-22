#!/Users/pranavmalhotra/anaconda2/bin/python

import sys
import csv

with open(sys.argv[1], 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	acc=[]
	pre=[]
	rec=[]
	for row in spamreader:
		acc.append(float(row[3]))
		pre.append(float(row[7]))
		rec.append(float(row[9]))

with open(sys.argv[2], 'a') as csvfile:
	writer=csv.writer(csvfile,delimiter=',')
	writer.writerow(acc)
	writer.writerow(pre)
	writer.writerow(rec)


