
import os
import multiprocessing
from multiprocessing import Pool
from functools import partial
import sys

def cvx_matlab(i, num_nodes, horizon, diffusion_type, fileToTrackProgress):
    import pdb; pdb.set_trace()
    fileToTrackProgress = fileToTrackProgress + '_' + str(i)
    arguments = str(i) + ', ' + str(num_nodes) + ', ' + str(horizon) + ', ' + str(diffusion_type) + ', ' + fileToTrackProgress
    os.system("matlab -nodesktop -nosplash -r 'parallel_cvx(" + arguments + ")'")

# Select the number of CPUs to use, if -1, use all of the available CPUs 
if int(sys.argv[1]) != -1:
    num_processors = int(sys.argv[1])
    pool = Pool(num_processors)
else:
    num_processors = multiprocessing.cpu_count()
    pool = Pool(num_processors)

num_nodes = int(sys.argv[2])
horizon = int(sys.argv[3])
diffusion_type = sys.argv[4]
fileToTrackProgress = sys.argv[5]

# Remove the .txt extension from the file
extension_file = fileToTrackProgress[-4:]
fileToTrackProgress = fileToTrackProgress[0:-4] + '_' + str(1) + extension_file
arguments = str(1) + ', ' + str(num_nodes) + ', ' + str(num_processors) + ', ' + str(horizon) + ", '" + str(diffusion_type) + "', " + "'" + fileToTrackProgress + "'"
os.system("matlab -nodesktop -nosplash -r \"parallel_cvx(" + arguments + ")\"")

# function = partial(cvx_matlab, num_nodes, horizon, diffusion_type, fileToTrackProgress)
# pool = Pool(num_processors)
# pool.map(function, range(1,num_processors + 1))
# pool.close()
# pool.join()
