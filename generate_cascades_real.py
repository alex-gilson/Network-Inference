import scipy.io
import numpy as np

n = 4   # Dataset number
# Load the data
filename = 'CRCNS/data/DataSet' + str(n) + '.mat'
data = scipy.io.loadmat(filename)['data']
NUMBER_NEURONS = data['nNeurons'][0][0][0][0]
N = NUMBER_NEURONS
simulation_duration = data['recordinglength'][0][0][0][0]
diffusion_type = 'rayleigh'

horizon = 20

num_cascades = np.zeros(N);
A_potential = np.zeros((N,N));
A_bad = np.zeros((N,N));
A_hat = np.zeros((N,N));

spikes = []

# This is needed to create a firings and indices file
for i in range(0,NUMBER_NEURONS):
    spikes.append(data['spikes'][0][0][i][0][0])

# Flatten the firing times from each of the neurons
firings = [item for sublist in spikes for item in sublist]

# Create the indices where each row is a different index
indices = [[i+1]*len(spikes[i]) for i in range(len(spikes))]

# Flatten the indices from each of the spikes
indices = [item for sublist in indices for item in sublist]

# Order the firings and indices chronologically
sort_idx = np.argsort(firings)
firings = [firings[sort_idx[i]] for i in range(len(firings))]
indices = [indices[sort_idx[i]] for i in range(len(indices))]

n = 0
m = 0
start = firings[n]
cascades = np.ones((int(simulation_duration/horizon),N))*(-1)

# Iterate through the simulation spikes
while start < simulation_duration:
    
    if n%10000 == 0:
        print(n)

    # define the window of observation
    start = firings[n] 
    end = start + horizon

    index = np.array(np.where((firings >= start) & (firings < end)))[0]

    firings_in_window = [firings[i] for i in index]
    firings_in_window = firings_in_window - start
    indices_in_window = [indices[i] for i in index]

    # initialise a cascade, non-fired with -1; assume all non-fired
    current_cascade = np.ones(NUMBER_NEURONS)*(-1)

    # first neuron to spike starts the cascade
    current_cascade[indices_in_window[0]-1] = 0

    # update cascade based on the rest of the firings
    for k in range(len(indices_in_window)):
        
        # Only the first firing is taken into account
        if current_cascade[indices_in_window[k]-1] == -1:
            current_cascade[indices_in_window[k]-1] = firings_in_window[k]    

    cascades[m] = current_cascade
    m = m + 1 

    # The index of the firing that starts the next cascade is the one following the last firing of this cascade 
    n = index[-1] + 1

# Delete the cascades with no entries (they were initialized with all -1s)
cascades = cascades[0:np.where(cascades == 0)[0][-1] + 1]


# Iterate through all the cascades
for c in range(len(cascades)):
    
    # Obtain the timing of the nodes that have fired
    idx = np.where(cascades[c] != -1)[0] # used nodes

    # Sort each cascade by earliest firing and keep the index order
    fired_nodes = [cascades[c,i] for i in idx]
    val = np.sort(fired_nodes)
    order = np.argsort(fired_nodes)

    if c%1000 == 0:
        print(c)

    # For all used nodes
    # Don't take the first value (it's value is 0, it belongs to the
    # stimulated node)
    for i in range(1,len(val)):
        
        # num_cascades stores the amount of times each node has fired
        num_cascades[idx[order[i]]] = num_cascades[idx[order[i]]] + 1

        for j in range(i-1):
            
            if diffusion_type == 'exp':
                A_potential[idx[order[j]], idx[order[i]]] = A_potential[idx[order[j]], idx[order[i]]] + val[i] - val[j]

            if (diffusion_type == 'pl') and (val[i] - val[j] > 1):
                A_potential[idx[order[j]], idx[order[i]]] = A_potential[idx[order[j]], idx[order[i]]] + np.log(val[i] - val[j])
                
            if diffusion_type == 'rayleigh':
                A_potential[idx[order[j]], idx[order[i]]] = A_potential[idx[order[j]], idx[order[i]]] + 0.5 * (val[i] - val[j])**2;


    for j in range(N):
        
        # If the node has spiked
        if np.where(idx==j)[0].shape[0] == 0:

            for i in range(len(val)):
                
                if diffusion_type == 'exp':
                    A_bad[idx[order[i]], j] = A_bad[idx[order[i]], j] + (horizon - val[i])
                if (diffusion_type == 'pl') and (horizon - val[i] > 1):
                    A_bad[idx[order[i]], j] = A_bad[idx[order[i]], j] + np.log(horizon - val[i])
                if diffusion_type == 'rayleigh':
                    A_bad[idx[order[i]], j] = A_bad[idx[order[i]], j] + 0.5*(horizon-val[i])**2;
            
        
        
np.savetxt("w/a_potential.csv", A_potential, delimiter=",")
np.savetxt("w/a_bad.csv", A_bad, delimiter=",")
np.savetxt("w/cascades.csv", cascades, delimiter=",")
np.savetxt("w/num_cascades.csv", num_cascades, delimiter=",")


print('Finished generating cascades')







