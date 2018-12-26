import time
import pickle

pickle_out = open('initial_time.pickle', 'wb')
intial_time = time.time()
pickle.dump(intial_time, pickle_out)

pickle_out.close()

