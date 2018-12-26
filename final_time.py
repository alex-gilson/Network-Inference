import time
import sys
import pickle
import datetime

final_time = time.time()
pickle_in = open('initial_time.pickle', 'rb')
initial_time = pickle.load(pickle_in)
elapsed_time = str(datetime.timedelta(seconds=(final_time - initial_time)))
print(elapsed_time)
pickle_in.close()


resultsFileName = sys.argv[1]

with open(resultsFileName,'a') as fd:
    fd.write('The algorithm took: ' + str(elapsed_time) + '\n')
