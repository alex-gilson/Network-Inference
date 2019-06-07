import time
import pickle
import sys

timeFileName = str(sys.argv[1])

initial_time = time.time()
pickle_out = open(timeFileName, 'wb')
pickle.dump(initial_time, pickle_out)
pickle_out.close()
