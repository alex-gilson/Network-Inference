#!/usr/bin/env


print('Running Brian Simulator...')

import sys
import numpy
from matplotlib import pyplot as plt
from brian2  import *
from utility import *

# extract command line arguments
seed=int(sys.argv[1])
N=int(sys.argv[2])
sparsity=float(sys.argv[3])
simulation_duration=int(sys.argv[4])
networkFileName=sys.argv[5]
firingsFileName=sys.argv[6]
indicesFileName=sys.argv[7]

# set the default seed
devices.device.seed(seed)

# suppress warnings
BrianLogger.suppress_hierarchy('brian2.codegen')

firings=[]
indices=[]

tau=1*ms

eqs= '''
dv/dt = (0.04*v*v + 5*v + 140 - u + I + stimulation)/tau : 1
du/dt = (a*(b*v-u))/tau : 1
I = 12*randn() : 1 (constant over dt)
a:1
b:1
c:1
d:1
stimulation:1
'''

threshold='v>30'

reset='''
v=c
u=u+d
'''

# Initialise the Neuron Group and set the Parameters
G = NeuronGroup(N,eqs,threshold=threshold,reset=reset,method='euler')
M = StateMonitor(G, 'v', record=0)
G.a = 0.02
G.b = 0.2
G.c = '-65+15*rand()**2'
G.d = '8-6*rand()**2'

# Define the connection values and the conditions
S = Synapses(G, G, 'w:1', on_pre='v_post += w')
S.connect(condition='i!=j', p=sparsity)
S.w='30*rand()'

# run the stimulation N number of times
# at each iteration, stimulate a different node
for stimulated_node in range(0,N):
	# reset v and u values
	G.v=-65
	G.u=G.b*G.v

	# only stimulate 1 node
	G.stimulation = 0
	G.stimulation[stimulated_node] = 3

	spikemon = SpikeMonitor(G)

	run(simulation_duration*ms)

	# store firings and indices
	firings.append(list(spikemon.i))
	indices.append(list(spikemon.t/ms))


# Write Network to File
myNetworkFile=open(networkFileName,'w')
for l in zip(S.i, S.j, S.w):
	myNetworkFile.write(",".join(map(str,l)))
	myNetworkFile.write("\n")
myNetworkFile.close()

# Write Firings to File
myFiringsFile=open(firingsFileName,'w')
for l in firings:
	myFiringsFile.write(",".join(map(str,l)))
	myFiringsFile.write("\n")
myFiringsFile.close()

# Write Indices to File
myIndicesFile=open(indicesFileName,'w')
for l in indices:
	myIndicesFile.write(",".join(map(str,l)))
	myIndicesFile.write("\n")
myIndicesFile.close()
