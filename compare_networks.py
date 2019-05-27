
import csv
import matplotlib.pyplot as plt
import sys
import numpy as np


N=int(sys.argv[1])
networkFileName=str(sys.argv[2])
matlab_or_python_graph=int(sys.argv[3])

S_hat = np.zeros((N,N))

# Open all the a_hat files to create the S_hat matrix
for i in range(N):
    filename = 'temporary/a_hat_' + str(i+1) + '.csv'
    S_hat[i] = np.genfromtxt(filename, delimiter=',')

inferred_network = S_hat
        

original_network=[[],[],[]]
with open(networkFileName, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		original_network[0].append(row[0])
		original_network[1].append(row[1])
		original_network[2].append(float(row[2])*20)

# inferred_network=[[],[],[]]
#
# with open(inferredNetworkFileName, 'rb') as csvfile:
# 	spamreader = csv.reader(csvfile, delimiter=',')
# 	for row in spamreader:
# 		if matlab_or_python_graph==0:
# 			inferred_network[0].append(int(row[0])-1)
# 			inferred_network[1].append(int(row[1])-1)
# 		else:
# 			inferred_network[0].append(int(row[0]))
# 			inferred_network[1].append(int(row[1]))
# 		inferred_network[2].append(40)

S=np.zeros((N,N),dtype=bool)
# S_hat=np.zeros((N,N),dtype=bool)

for i,j in zip(original_network[0],original_network[1]):
	S[int(i),int(j)]=True;

# for i,j in zip(inferred_network[0],inferred_network[1]):
	# S_hat[int(i),int(j)]=True;

mae = np.mean(abs(S_hat[np.where(S!=0)]-S[np.where(S!=0)])/S[np.where(S!=0)])

if np.sum(S_hat)==0:
	precision=0
else:
	precision=float(np.sum(np.logical_and(S,S_hat)))/np.sum(S_hat)
recall=float(np.sum(np.logical_and(S,S_hat)))/np.sum(S)
accuracy=1-float(np.sum(np.logical_xor(S,S_hat)))/(np.sum(S)+np.sum(S_hat))

results = np.array([accuracy, mae, precision, recall])

np.savetxt("temporary/results.csv", results, delimiter=",")


plt.figure(figsize=(10,7))
plt.scatter(original_network[1],original_network[0], original_network[2],c='b',label='Original Network')
if matlab_or_python_graph==0:
	plt.scatter(inferred_network[1],inferred_network[0], inferred_network[2], c='r',label='Matlab Inferred Network')
	title='Matlab Results, Accuracy: {}, Precision: {}, Recall: {}'.format(round(accuracy,3), round(precision,3), round(recall,3))
	plt.suptitle(title, fontsize=14, fontweight='bold')
else:
	plt.scatter(inferred_network[1],inferred_network[0], inferred_network[2], c='g',label='Python Inferred Network')
	title='Python Results, Accuracy: {}, Precision: {}, Recall: {}'.format(round(accuracy,3), round(precision,3), round(recall,3))
	plt.suptitle(title, fontsize=14, fontweight='bold')

plt.xlabel('Target neuron index')
plt.ylabel('Source neuron index')
plt.xlim(-0.5, N-0.5)
plt.ylim(-0.5, N-0.5)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2,  borderaxespad=0.)

plt.show()           
