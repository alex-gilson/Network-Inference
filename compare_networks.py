
import csv
# import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy import stats
import time
import pickle
import multiprocessing
import pandas as pd
import datetime

matlab_or_python_graph=int(sys.argv[1])
aHatFileName=str(sys.argv[2])
resultsFileName = str(sys.argv[3])
seed = int(sys.argv[4])
num_nodes = int(sys.argv[5])
sparsity = float(sys.argv[6])
networkFileName = str(sys.argv[7])
firingsFileName = str(sys.argv[8])
indicesFileName = str(sys.argv[9])
inferredNetworkFileName = sys.argv[10]
horizon = float(sys.argv[11])
diffusion_type = str(sys.argv[12])
stimulation_mode = str(sys.argv[13])
num_processors = str(sys.argv[14])
timeFileName = str(sys.argv[15])

N = num_nodes

# Select the number of CPUs to use, if -1, use all of the available CPUs 
if int(sys.argv[14]) != -1:
    num_processors = int(sys.argv[14])
else:
    num_processors = multiprocessing.cpu_count()

S_hat = np.zeros((N,N))
S = np.zeros((N,N))
S_hat_boolean = np.zeros((N,N),dtype=bool)
S_boolean = np.zeros((N,N),dtype=bool)

original_network=[[],[],[]]
with open(networkFileName, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
            original_network[0].append(row[0])
            original_network[1].append(row[1])
            original_network[2].append(float(row[2]))

for i,j,k in zip(original_network[0],original_network[1], original_network[2]):
    S[int(i),int(j)] = k;

# Open all the a_hat files to create the S_hat matrix
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

# Compute mae
mae = np.mean(abs(S_hat[np.where(S!=0)]-S[np.where(S!=0)])/S[np.where(S!=0)])

# Convert S into a boolean array
S_boolean[np.where(S>0)] = True

# Convert S_hat into a boolean array
S_hat_boolean[np.where(S_hat>0)] = True

if np.sum(S_hat) == 0:
	precision=0
else:
	precision=float(np.sum(np.logical_and(S_boolean,S_hat_boolean)))/np.sum(S_hat_boolean)

recall = float(np.sum(np.logical_and(S_boolean,S_hat_boolean)))/np.sum(S_boolean)
accuracy = 1 - float(np.sum(np.logical_xor(S_boolean,S_hat_boolean)))/(np.sum(S_boolean)+np.sum(S_hat_boolean))

results = np.array([accuracy, mae, precision, recall])

# np.savetxt("temporary/results.csv", results, delimiter=",")
np.savetxt(inferredNetworkFileName, inferred_network, delimiter=",")

print('MAE: ', mae)
print('Precision: ', precision)
print('Recall: ', recall)
print('Accuracy: ', accuracy)

final_time = time.time()
pickle_in = open(timeFileName, 'rb')
initial_time = pickle.load(pickle_in)
elapsed_time = str(datetime.timedelta(seconds=(final_time - initial_time)))
pickle_in.close()

# data = np.genfromtxt('temporary/results.csv', delimiter=',')
# data = data[-1,:].reshape(-1,1)
d = {'seed': [seed], 'num_nodes': [num_nodes], 'elapsed_time': [elapsed_time], 'num_processors': [num_processors],'accuracy': results[0], 'MAE': results[1], 'precision': results[2], 'recall': results[3], 'sparsity': [sparsity],  'horizon': [horizon],'diffusion_type':[diffusion_type], 'stimulation_mode': [stimulation_mode], 'date': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M")]}
df = pd.DataFrame(d)
df.to_csv(resultsFileName, mode='a', header=True)

# plt.figure(figsize=(10,7))
# plt.scatter(original_network[1],original_network[0], original_network[2],c='b',label='Original Network')
# if matlab_or_python_graph==0:
# 	plt.scatter(inferred_network[1],inferred_network[0], inferred_network[2], c='r',label='Matlab Inferred Network')
# 	title='Matlab Results, Accuracy: {}, Precision: {}, Recall: {}'.format(round(accuracy,3), round(precision,3), round(recall,3))
# 	plt.suptitle(title, fontsize=14, fontweight='bold')
# else:
# 	plt.scatter(inferred_network[1],inferred_network[0], inferred_network[2], c='g',label='Python Inferred Network')
# 	title='Python Results, Accuracy: {}, Precision: {}, Recall: {}'.format(round(accuracy,3), round(precision,3), round(recall,3))
# 	plt.suptitle(title, fontsize=14, fontweight='bold')
#
# plt.xlabel('Target neuron index')
# plt.ylabel('Source neuron index')
# plt.xlim(-0.5, N-0.5)
# plt.ylim(-0.5, N-0.5)
# plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#            ncol=2,  borderaxespad=0.)
# plt.show()           
