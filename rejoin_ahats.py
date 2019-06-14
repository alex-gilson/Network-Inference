
from __future__ import division
import numpy as np
import sys
import scipy.io
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

dataset = int(sys.argv[1])
aHatFileName = str(sys.argv[2])
inferredNetworkFileName = str(sys.argv[3])

filename = 'CRCNS/data/DataSet' + str(dataset) + '.mat'
N = scipy.io.loadmat(filename)['data']['nNeurons'][0][0][0][0]
x_array = scipy.io.loadmat(filename)['data']['x'][0][0][0]
y_array = scipy.io.loadmat(filename)['data']['y'][0][0][0]


S_hat = np.zeros((N,N))

for i in range(N):
    filename = aHatFileName + str(i+1) + '.csv'
    S_hat[i] = np.genfromtxt(filename, delimiter=',')

# Transpose the inferred matrix
S_hat = S_hat.T

# Convert NaN to zeros
S_hat[np.where(np.isnan(S_hat))] = 0

# Remove values very close to zero
S_hat[np.where(S_hat <= np.percentile(S_hat,99, interpolation='lower'))] = 0

S_hat = np.interp(S_hat, np.linspace(S_hat.min(),S_hat.max(),1000), np.linspace(0,30,1000))

# S_hat[np.where(S_hat < 5)] = 0

DG = nx.DiGraph()

for i in range(N):
    DG.add_node(i, pos=(x_array[i], y_array[i]))

inferred_network = []
for i, row in enumerate(S_hat):
    for j, col in enumerate(row):
        if col != 0:
            inferred_network.append([int(i), int(j), col])
            DG.add_weighted_edges_from([(int(j),int(i),col)])

np.savetxt(inferredNetworkFileName, inferred_network, delimiter=",")

pos=nx.get_node_attributes(DG,'pos')
nx.draw(DG,pos, node_color='blue')
plt.show()


