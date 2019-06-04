import os
import multiprocessing
from multiprocessing import Pool
from functools import partial
import numpy as np
import sys

num_processors = int(sys.argv[1])
num_nodes = int(sys.argv[2])
horizon = int(sys.argv[3])
diffusion_type = str(sys.argv[4])
cascadesFileName = str(sys.argv[5])
aBadFileName = str(sys.argv[6])
aPotentialFileName = str(sys.argv[7])
numCascadesFileName = str(sys.argv[8])


# Algorithm to distribute nodes between processors as a function of the number of cascades
processor_list = []
num_cascades = np.loadtxt(numCascadesFileName,delimiter=',').astype(int)
print('Number of cascades:')
print(num_cascades)
idxs = np.argsort(num_cascades)[::-1]
k = 0

for idx in idxs:
   # Each processor will have the num_processors first largest values 
   if k < num_processors:
       # Steps required to create a list of lists
       processor_list.append(idx)
       processor_list[k] = []
       processor_list[k].append(idx)
       k = k + 1
   else:
       sum_array = np.zeros(num_processors) 
       for n in range(0, num_processors):
           sum_array[n] = sum(num_cascades[processor_list[n]]) 
       argmin = np.argmin(sum_array)
       processor_list[argmin].append(idx)

def cvx_matlab(i, num_nodes=num_nodes, horizon=horizon, diffusion_type=diffusion_type, processor_list=processor_list):
    print('Number of processors: ')
    print(num_processors)
    arguments = ''
    # Tell matlab what nodes to compute 
    nodes = processor_list[i-1]        
    # To reduce RAM consumption make the algorithm spread the most memory expensive nodes throughout the computation period
    # If the processor number is even, start computing the nodes with the least number of cascades
    if i%2 == 0:
        nodes = nodes[::-1]
    arguments = str(nodes) + ', ' + str(num_nodes) + ', ' + str(num_processors) + ', ' + str(horizon) + ", '" + str(diffusion_type) + "', '" + str(cascadesFileName) + "', '" + str(aBadFileName) + "', '" + str(aPotentialFileName) + "', '" + str(numCascadesFileName) + "'"
    print(arguments)
    os.system("matlab -nodesktop -nosplash -r \"parallel_cvx(" + arguments + ");exit;\"")

# Select the number of CPUs to use, if -1, use all of the available CPUs 
if int(sys.argv[1]) != -1:
    num_processors = int(sys.argv[1])
    pool = Pool(num_processors)
else:
    num_processors = multiprocessing.cpu_count()
    pool = Pool(num_processors)


# function = partial(cvx_matlab, num_nodes, horizon, diffusion_type, fileToTrackProgress)
# pool = Pool(num_processors)

pool.map(cvx_matlab, range(1,num_processors + 1))
pool.close()
pool.join()
