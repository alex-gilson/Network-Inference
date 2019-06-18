
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

path = 'r/sim_times_2/network_5_nodes/network_stimulation_random_spikes_stimulation_time_1000_4/'

simulation_times = [250, 500, 750, 1000, 1250, 1500]
seeds = [1,2,3,4]
network_sizes = [5,10,15,20]
maes = np.zeros((len(network_sizes), len(simulation_times), len(seeds)))
accuracies = np.zeros((len(network_sizes), len(simulation_times), len(seeds)))
precisions = np.zeros((len(network_sizes), len(simulation_times), len(seeds)))
recalls = np.zeros((len(network_sizes), len(simulation_times), len(seeds)))

for a, n in enumerate(network_sizes):
    for b, time in enumerate(simulation_times):
        for c, s in enumerate(seeds):
            path = 'r/sim_times_2/network_' + str(n) + '_nodes/network_stimulation_random_spikes_stimulation_time_' + str(time) + '_4/' + 'results_' + str(s) + '.csv'
            if os.path.exists(path):
                with open(path, 'r') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',')
                    results = []
                    for row in spamreader:
                        results.append(row)
                    maes[a,b,c] = float(results[-1][1])
                    accuracies[a,b,c] = float(results[-1][2])
                    precisions[a,b,c] = float(results[-1][9])
                    recalls[a,b,c] = float(results[-1][10])
            else:
                print('Missing results for network size: ' + str(n) + ' nodes, simulation time: ' + str(time) + ', seed: ' + str(s))
                maes[a,b,c] = np.nan
                accuracies[a,b,c] = np.nan
                precisions[a,b,c] = np.nan
                recalls[a,b,c] = np.nan


for n, size in enumerate(network_sizes):

    plt.figure()
    plt.plot(simulation_times, np.mean(maes[n], axis=1), label='MAE')
    plt.plot(simulation_times, np.mean(accuracies[n], axis=1), label='accuracy')
    plt.plot(simulation_times, np.mean(precisions[n], axis=1), label='precision')
    plt.plot(simulation_times, np.mean(recalls[n], axis=1), label='recall')
    plt.legend()
    plt.grid()
    plt.xlabel('length of simulation (s)')
    plt.title('Simulation results for a network of ' + str(size) + ' neurons')
    plt.savefig('plot/results_' + str(size) + '_neurons.pdf', dpi=300)
    plt.show()

# for n, time in enumerate(simulation_times):
#
#     plt.figure()
#     import pdb; pdb.set_trace()
#     plt.plot(simulation_times, np.mean(maes[:,n,:], axis=0), label='MAE')
#     plt.plot(simulation_times, np.mean(accuracies[:,n,:], axis=0), label='accuracy')
#     plt.plot(simulation_times, np.mean(precisions[:,n,:], axis=0), label='precision')
#     plt.plot(simulation_times, np.mean(recalls[:,n,:], axis=0), label='recall')
#     plt.legend()
#     plt.grid()
#     plt.xlabel('length of simulation (s)')
#     plt.title('Average performance of networks of different sizes')
#     plt.savefig('plot/results_times_neurons.pdf', dpi=300)
#     plt.show()
# plt.figure()
# plt.plot(network_sizes, np.mean(np.mean(maes, axis=2), axis=1), label = 'MAE')
# plt.plot(network_sizes, np.mean(np.mean(accuracies, axis=2), axis=1), label = 'accuracy')
# plt.plot(network_sizes, np.mean(np.mean(precisions, axis=2), axis=1), label = 'precision')
# plt.plot(network_sizes, np.mean(np.mean(recalls, axis=2), axis=1), label = 'recall')
# plt.legend()
# plt.grid()
# plt.xlabel('number of neurons')
# plt.title('Size of the network effect on performance')
# plt.savefig('plot/size_effect_performance.pdf', dpi=300)
# plt.show()

plt.figure()
x = np.arange(4)
bars = [np.mean(maes[1],axis=1)[-1], np.mean(accuracies[-1],axis=1)[-1], np.mean(precisions[1],axis=1)[-1], np.mean(recalls[1],axis=1)[-1]]
barlist = plt.bar(x,bars)
barlist[0].set_color('#5a3aa9')
barlist[1].set_color('#00a0ff')
barlist[2].set_color('#8b9dc3')
barlist[3].set_color('#eb104e')
plt.xticks(x, ['MAE', 'Accuracy', 'Precision', 'Recall'])
plt.title('Average performance of NetRate')
plt.grid()
plt.savefig('plot/proof_suitability.pdf', dpi=300)
plt.show()

