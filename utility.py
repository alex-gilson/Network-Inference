#!/usr/bin/env
#
# from brian2 import *
# import csv
# import matplotlib.pyplot as plt
# import sys
# import numpy as np
# import networkx as nx
#
#
# def visualise_connectivity(S):
#     Ns = len(S.source)
#     Nt = len(S.target)
#     figure(figsize=(10, 4))
#     subplot(121)
#     plot(zeros(Ns), arange(Ns), 'ok', ms=10)
#     plot(ones(Nt), arange(Nt), 'ok', ms=10)
#     for i, j in zip(S.i, S.j):
#         plot([0, 1], [i, j], '-k')
#     xticks([0, 1], ['Source', 'Target'])
#     ylabel('Neuron index')
#     xlim(-0.1, 1.1)
#     ylim(-1, max(Ns, Nt))
#     subplot(122)
#     scatter(S.i, S.j, S.w*20)
#     xlim(-1, Ns)
#     ylim(-1, Nt)
#     xlabel('Source neuron index')
#     ylabel('Target neuron index')
#     show()
#
# def raster_plot(spikemon):
#     plot(spikemon.t/ms, spikemon.i, '.k')
#     xlabel('Time (ms)')
#     ylabel('Neuron index');
#     show()
#
# def visualise_simple(networkFileName):
#     original_network=[[],[],[]]
#     with open(networkFileName, 'rb') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=',')
#         for row in spamreader:
#             original_network[0].append(row[0])
#             original_network[1].append(row[1])
#             original_network[2].append(float(row[2])*20)
#     original_network = np.asarray(original_network)
#     original_network[0] = np.add(original_network[0].astype(int),np.ones(len(original_network[0])))
#     original_network[1] = np.add(original_network[1].astype(int),np.ones(len(original_network[1])))
#     plt.figure(figsize=(10,7))
#     plt.grid('--',linewidth=1, zorder=-1) 
#     plt.scatter(original_network[0],original_network[1], original_network[2].astype(float),c='b',label='Original Network', zorder=1)
#     plt.xlabel('Source neuron index')
#     plt.ylabel('Target neuron index')
#     plt.xlim([0,21])
#     plt.ylim([0,21])
#     plt.xticks(np.arange(1, 21, step=1))
#     plt.yticks(np.arange(1, 21, step=1))
#     plt.title('Network of 20 nodes')
#     # plt.set_axisbelow(True)
#     plt.show()           
#
#     # # # Generating sample data
#     # # G = nx.florentine_families_graph()
#     # # adjacency_matrix = nx.adjacency_matrix(G)
#     # #
#     # # The actual work
#     # # You may prefer `nx.from_numpy_matrix`.
#     # G2 = nx.from_scipy_sparse_matrix(adjacency_matrix)
#     # import pdb; pdb.set_trace()
#     # nx.draw_circular(G2)
#     # plt.axis('equal')
#     # plt.show()
#     #
# if __name__ == "__main__":
#     visualise_simple(sys.argv[1])
