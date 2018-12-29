import time
import multiprocessing
import pandas as pd
import sys
import pickle
import datetime
from numpy import genfromtxt

resultsFileName = sys.argv[1]
seed = int(sys.argv[2])
num_nodes = int(sys.argv[3])
sparsity = float(sys.argv[4])
networkFileName = sys.argv[5]
firingsFileName = sys.argv[6]
indicesFileName = sys.argv[7]
matlabNetworkFileName = sys.argv[8]
fileToTrackProgress = sys.argv[9]
horizon = float(sys.argv[10])

# Select the number of CPUs to use, if -1, use all of the available CPUs 
if int(sys.argv[11]) != -1:
    num_processors = int(sys.argv[11])
else:
    num_processors = multiprocessing.cpu_count()
# seed=1
# num_nodes=10
# sparsity=0.1
# simulation_duration=4000
# networkFileName='r/for_histogram/network_sim_time_1000/network_seed_1.csv'
# firingsFileName='w/firing.csv'
# indicesFileName='w/indice.csv'
# matlabNetworkFileName ='r/for_histogram/network_sim_time_4000/network_seed_1.csv';
# fileToTrackProgress='r/for_histogram/network_sim_time_4000/progress_tracker_seed_1.txt'
# diffusion_type='rayleigh'
# horizon=100
# num_processors=3
# elapsed_time = 123456 
# resultsFileName = 'test.csv'
#
final_time = time.time()
pickle_in = open('initial_time.pickle', 'rb')
initial_time = pickle.load(pickle_in)
elapsed_time = str(datetime.timedelta(seconds=(final_time - initial_time)))
pickle_in.close()

data = genfromtxt('temporary/accuracy.csv', delimiter=',')
# data = data[-1,:].reshape(-1,1)
d = {'seed': [seed], 'num_nodes': [num_nodes], 'elapsed_time': [elapsed_time], 'num_processors': [num_processors],'accuracy': data[0], 'MAE': data[1], 'precision': data[2], 'recall': data[3], 'num_cascades': data[4], 'sparsity': [sparsity],  'horizon': [horizon],'networkFileName': [networkFileName], 'firingsFileName': [firingsFileName], 'indicesFileName': [indicesFileName], 'matlabNetworkFileName': [matlabNetworkFileName], 'fileToTrackProgress': [fileToTrackProgress]}
df = pd.DataFrame(d)
df.to_csv(resultsFileName, mode='a', header=False)


