
from __future__ import division
import numpy as np
import sys
import scipy.io
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
from colour import Color

dataset = int(sys.argv[1])
aHatFileName = str(sys.argv[2])
inferredNetworkFileName = str(sys.argv[3])
N = int(sys.argv[4])
plot = True

if dataset != 0:
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

if dataset != 0 and plot:
    DG = nx.DiGraph()
    for i in range(N):
        DG.add_node(i, pos=(x_array[i], y_array[i]))

inferred_network = []
color_map = []
red = Color('#f64f59')
colours = list(red.range_to(Color("#12c2e9"),7))
for i, row in enumerate(S_hat):
    for j, col in enumerate(row):
        if col != 0:
            inferred_network.append([int(i), int(j), col])
            if dataset != 0 and plot:
                DG.add_weighted_edges_from([(int(j),int(i),col)])

np.savetxt(inferredNetworkFileName, inferred_network, delimiter=",")


if plot:
    senders = np.array(DG.edges)[:,0]
    senders_count = np.bincount(senders,minlength=N)
    receivers = np.array(DG.edges)[:,1]
    receivers_count = np.bincount(receivers,minlength=N)
    count = senders_count - receivers_count

    # Plot Indegree
    plt.figure()
    bins = np.linspace(0, 15, 12)
    plt.hist(senders_count,bins, label='outdegree', color='red', alpha=0.5)
    plt.hist(receivers_count,bins, label='indegree', color='blue', alpha=0.5)
    plt.xlabel('number of connections')
    plt.ylabel('number of occurrences')
    plt.title('Indegree and outdegree of the biological neural network')
    plt.grid()
    plt.legend()
    plt.savefig('plot/degree_histogram_real_network.pdf', dpi=300)
    plt.show()

    import pdb; pdb.set_trace()

    for i in count:
        if i <= -3:
            color_map.append(str(colours[0]))
        elif i == -2:
            color_map.append(str(colours[1]))
        elif i == -1:
            color_map.append(str(colours[2]))
        elif i == 0:
            color_map.append(str(colours[3]))
        elif i == 1:
            color_map.append(str(colours[4]))
        elif i == 2:
            color_map.append(str(colours[5]))
        elif i >= 3:
            color_map.append(str(colours[6]))
        
    if dataset != 0:
        pos=nx.get_node_attributes(DG,'pos')
        nx.draw(DG,pos, node_color=color_map)
        plt.savefig('plot/crcns_4_60_xy.pdf', dpi=300)
        plt.title('Connectivity of a biological neural network')
        plt.show()


