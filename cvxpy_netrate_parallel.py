#!/usr/bin/env

from __future__ import division
import numpy as np
from cvxpy import *
from scipy import stats
from multiprocessing import Pool
import sys

# define number of nodes
#num_nodes=int(sys.argv[1])
num_nodes=10
# file to write network to
#python_network=sys.argv[2]
python_network='inferred_network.csv'
# set printing precision
np.set_printoptions(precision=2)

# import all data and store as numpy matrices
with open ("w/cascades.csv", "r") as myfile:
    cascades_text=myfile.read()
    cascades = np.matrix(cascades_text)

with open ("w/a_bad.csv", "r") as myfile:
	A_bad_text=myfile.read()
	A_bad = np.matrix(A_bad_text)

with open ("w/a_potential.csv", "r") as myfile:
	A_potential_text=myfile.read()
	A_potential = np.matrix(A_potential_text)

with open ("w/num_cascades.csv", "r") as myfile:
	num_cascades_text=myfile.read()
	num_cascades = np.matrix(num_cascades_text)

with open ("w/S_matrix.csv", "r") as myfile:
	S_text=myfile.read()
	S = np.matrix(S_text)

# initialise array to hold results
S_hat=np.random.randn(num_nodes,num_nodes)

def solve_individual_problem(solving_for_node):
	a_hat = Variable(num_nodes)
	t_hat = Variable(num_cascades.item(solving_for_node))

	# the objective function that we want to minimize
	obj=0

	# initialise the list of constraints
	constraints=[]

	# first constraint: each value of a_hat has to be positive
	constraints.append(a_hat >= 0)

	# considering all the observed cascades, if node j never fired before node i
	# place the constraint that there is no connection from node j to i
	for i in range(0,num_nodes):
		constraints.append(a_hat[A_potential.item(i,solving_for_node)==0] == 0)

	# adding log survival functions to the objective function
	for j in range(0,num_nodes):
	    if A_potential.item(j,solving_for_node) > 0:
	        obj = -a_hat[j]*(A_potential.item(j,solving_for_node) + A_bad.item(j,solving_for_node)) + obj

	# counting variable for next loop
	c_act = 0;

	for c in range(0,len(cascades)):
		# skip if the node that we are solving for does not participate in this cascade
		# or if the node was the starting point for this cascade
		if cascades[c,solving_for_node]==-1 or cascades[c,solving_for_node]==0:
			continue

		args=np.argsort(cascades[c,:])
		a=np.where(args[0,:]==solving_for_node)

		# placing constraint on the hazard functions
		x=0;
		for i in range(0,a[1][0]):
			x=x+a_hat[i]
			
		constraints.append(t_hat[c_act]==x)

		# add the hazard functions to the object function
		obj = obj + log(t_hat[c_act])
		c_act = c_act + 1

	# defining the convex optimization problem
	prob = Problem(Maximize(obj),constraints)
	# solve the problem using the SCS solver
	prob.solve(solver="SCS",verbose=False,max_iters=40000)

	return np.squeeze(a_hat.value)*100

solving_for_node=range(0,num_nodes)
pool=Pool(processes=10)	
S_hat=np.squeeze(np.array(pool.map(solve_individual_problem,solving_for_node))).transpose()

S_hat=stats.threshold(S_hat, threshmin=0.01, threshmax=1, newval=0)

# Write Indices to File
myNetworkFile=open(python_network,'w')
for i, row in enumerate(S_hat):
	for j, col in enumerate(row):
		if col != 0:
			l=[i,j,col]
			# print l
			myNetworkFile.write(",".join(map(str,l)))
			myNetworkFile.write("\n")
myNetworkFile.close()
