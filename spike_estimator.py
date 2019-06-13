import csv
import numpy as np

TRAIN_TEST_SPLIT = 50

indicesFileName = "/home/alex/Documents/Final-Year-Project/r/network_10_nodes/network_stimulation_random_spikes_stimulation_time_100_4/indices_1.csv"
firingsFileName = "/home/alex/Documents/Final-Year-Project/r/network_10_nodes/network_stimulation_random_spikes_stimulation_time_100_4/firings_1.csv"

indices = []
firings = []

with open(indicesFileName, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        indices.append(row)

with open(firingsFileName, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        firings.append(row)


spikes = []

# Flatten the firing times from each of the neurons
firings = np.array([item for sublist in firings for item in sublist]).astype(float)

# Flatten the firing times from each of the neurons
indices = np.array([item for sublist in indices for item in sublist]).astype(float)

# Order the firings and indices chronologically
sort_idx = np.argsort(firings)
firings = np.array([firings[sort_idx[i]] for i in range(len(firings))])
indices = np.array([indices[sort_idx[i]] for i in range(len(indices))]).astype(int)

time_cuttoff = len(firings)*(TRAIN_TEST_SPLIT/100)
import pdb; pdb.set_trace()

