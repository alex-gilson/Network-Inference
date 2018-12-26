import time
import pickle

initial_time = time.time()
pickle_out = open('initial_time.pickle', 'wb')
pickle.dump(initial_time, pickle_out)
pickle_out.close()
