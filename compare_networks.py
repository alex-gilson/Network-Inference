
import csv
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy import stats

N=int(sys.argv[1])
networkFileName=str(sys.argv[2])
matlab_or_python_graph=int(sys.argv[3])

S_hat = np.zeros((N,N))
S = np.zeros((N,N))
S_hat_boolean = np.zeros((N,N),dtype=bool)
S_boolean = np.zeros((N,N),dtype=bool)

# Open all the a_hat files to create the S_hat matrix
for i in range(N):
    filename = 'temporary/a_hat_' + str(i+1) + '.csv'
    S_hat[i] = np.genfromtxt(filename, delimiter=',')

# Convert NaN to zeros
S_hat[np.where(np.isnan(S_hat))] = 0

# Remove values very close to zero (unfeasible rate)
import pdb; pdb.set_trace()
S_hat[np.where(S_hat <= np.percentile(S_hat,90, interpolation='lower'))] = 0

# S_hat[np.where(S_hat<np.median(S_hat))] = 0
# S_hat[np.where(S_hat<np.sort(S.flatten())[int((S.flatten().shape[0]-1)/10)])] = 0

S_hat = np.interp(S_hat.T, np.linspace(S_hat.min(),S_hat.max(),1000), np.linspace(0,30,1000))



original_network=[[],[],[]]
with open(networkFileName, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		original_network[0].append(row[0])
		original_network[1].append(row[1])
		original_network[2].append(float(row[2]))


inferred_network = []
for i, row in enumerate(S_hat):
    for j, col in enumerate(row):
        if col != 0:
            inferred_network.append([j, i, col])



for i,j,k in zip(original_network[0],original_network[1], original_network[2]):
    S[int(i),int(j)] = k;

# for i,j in zip(inferred_network[0],inferred_network[1]):
	# S_hat[int(i),int(j)]=True;


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

np.savetxt("temporary/results.csv", results, delimiter=",")

print('MAE: ', mae)
print('Precision: ', precision)
print('Recall: ', recall)
print('Accuracy: ', accuracy)



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
