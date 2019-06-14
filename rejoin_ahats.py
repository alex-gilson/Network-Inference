
import numpy as np
import sys
import scipy.io
from __future__ import division
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

dataset = int(sys.argv[1])
aHatFileName = str(sys.argv[2])
inferredNetworkFileName = str(sys.argv[3])

filename = 'CRCNS/data/DataSet' + str(dataset) + '.mat'
N = scipy.io.loadmat(filename)['data']['nNeurons'][0][0][0][0]

S_hat = np.zeros((N,N))

for i in range(N):
    filename = aHatFileName + str(i+1) + '.csv'
    S_hat[i] = np.genfromtxt(filename, delimiter=',')

# Transpose the inferred matrix
S_hat = S_hat.T

# Convert NaN to zeros
S_hat[np.where(np.isnan(S_hat))] = 0

# Remove values very close to zero
S_hat[np.where(S_hat <= np.percentile(S_hat,90, interpolation='lower'))] = 0

S_hat = np.interp(S_hat, np.linspace(S_hat.min(),S_hat.max(),1000), np.linspace(0,30,1000))

# S_hat[np.where(S_hat < 5)] = 0


inferred_network = []
for i, row in enumerate(S_hat):
    for j, col in enumerate(row):
        if col != 0:
            inferred_network.append([int(i), int(j), col])

np.savetxt(inferredNetworkFileName, inferred_network, delimiter=",")


G = nx.generators.directed.random_k_out_graph(10, 3, 0.5)
pos = nx.layout.spring_layout(G)

node_sizes = [3 + 10 * i for i in range(len(G))]
M = G.number_of_edges()
edge_colors = range(2, M + 2)
edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->', arrowsize=10, edge_color=edge_colors, edge_cmap=plt.cm.Blues, width=2)

# set alpha value for each edge
for i in range(M):
    edges[i].set_alpha(edge_alphas[i])

pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
pc.set_array(edge_colors)
plt.colorbar(pc)

ax = plt.gca()
ax.set_axis_off()
plt.show()



