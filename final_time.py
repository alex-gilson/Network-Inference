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
horizon = float(sys.argv[9])
diffusion_type = str(sys.argv[10])
stimulation_mode = str(sys.argv[11])

# Select the number of CPUs to use, if -1, use all of the available CPUs 
if int(sys.argv[11]) != -1:
    num_processors = int(sys.argv[11])
else:
    num_processors = multiprocessing.cpu_count()

final_time = time.time()
pickle_in = open('initial_time.pickle', 'rb')
initial_time = pickle.load(pickle_in)
elapsed_time = str(datetime.timedelta(seconds=(final_time - initial_time)))
pickle_in.close()

data = genfromtxt('temporary/results.csv', delimiter=',')
# data = data[-1,:].reshape(-1,1)
d = {'seed': [seed], 'num_nodes': [num_nodes], 'elapsed_time': [elapsed_time], 'num_processors': [num_processors],'accuracy': data[0], 'MAE': data[1], 'precision': data[2], 'recall': data[3], 'sparsity': [sparsity],  'horizon': [horizon],'diffusion_type':[diffusion_type], 'stimulation_mode': [stimulation_mode]}
df = pd.DataFrame(d)
df.to_csv(resultsFileName, mode='a', header=True)


