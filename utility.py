#!/Users/pranavmalhotra/anaconda2/bin/python

from brian2 import *
import csv
import matplotlib.pyplot as plt
import sys

def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    scatter(S.i, S.j, S.w*20)
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')
    show()

def raster_plot(spikemon):
    plot(spikemon.t/ms, spikemon.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index');
    show()

def visualise_simple(networkFileName):
    original_network=[[],[],[]]
    with open(networkFileName, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            original_network[0].append(row[0])
            original_network[1].append(row[1])
            original_network[2].append(float(row[2])*20)
    plt.figure(figsize=(10,7))
    plt.scatter(original_network[0],original_network[1], original_network[2],c='b',label='Original Network')
    plt.xlabel('Source neuron index')
    plt.ylabel('Target neuron index')
    plt.show()           


if __name__ == "__main__":
    visualise_simple(sys.argv[1])