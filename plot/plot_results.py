
import numpy as np
import matplotlib.pyplot as plt

mae_10 = []
acc_10 = []
prec_10 = []
rec_10 = []
mae_10.append([0.99, 0.99, 0.99, 0.99, 0.99])
acc_10.append([0.08, 0.125, 0.1, 0.11, 0])
prec_10.append([0.1, 0.1, 0.1, 0.1, 0])
rec_10.append([0.07, 0.17, 0.1, 0.13, 0])

mae_10.append([0.99, 0.99, 0.99, 0.99, 0.99])
acc_10.append([0.16, 0.125, 0.1, 0.22, 0])
prec_10.append([0.2, 0.1, 0.1, 0.2, 0])
rec_10.append([0.13, 0.17, 0.1, 0.25, 0])

mae_10.append([0.96, 0.99, 0.99, 0.99, 0.99])
acc_10.append([0.16, 0.125, 0.1, 0.22, 0])
prec_10.append([0.2, 0.1, 0.1, 0.2, 0])
rec_10.append([0.13, 0.17, 0.1, 0.25, 0])

mae_20 = []
acc_20 = []
prec_20 = []
rec_20 = []


mae_20.append([0.99, 0.99, 0.98, 0.99, 0.99])
acc_20.append([0.02, 0.1, 0.08, 0.07, 0.17])
prec_20.append([0.03, 0.1, 0.08, 0.08, 0.18])
rec_20.append([0.03, 0.1, 0.08, 0.07, 0.16])

mae_20.append([0.99, 0.99, 0.98, 0.99, 0.99])
acc_20.append([0.02, 0.1, 0.1, 0.07, 0.17])
prec_20.append([0.03, 0.1, 0.1, 0.08, 0.18])
rec_20.append([0.03, 0.1, 0.11, 0.07, 0.16])

mae_20.append([0.99, 0.99, 0.98, 0.99, 0.99])
acc_20.append([0.02, 0.1, 0.1, 0.07, 0.17])
prec_20.append([0.03, 0.1, 0.1, 0.08, 0.18])
rec_20.append([0.03, 0.1, 0.11, 0.07, 0.16])

mae_10 = np.array(mae_10)
mae_20 = np.array(mae_20)
acc_10 = np.array(acc_10)
acc_20 = np.array(acc_20)
prec_10 = np.array(prec_10)
prec_20 = np.array(prec_20)
rec_10 = np.array(rec_10)
rec_20 = np.array(rec_20)



plt.figure()
# plt.plot([500,1000,1500], np.mean(mae_10, axis=1), label='MAE')
plt.plot([500,1000,1500], np.mean(acc_10, axis=1), label='accuracy')
plt.plot([500,1000,1500], np.mean(prec_10, axis=1), label='precision')
plt.plot([500,1000,1500], np.mean(rec_10, axis=1), label='recall')
plt.legend()
plt.grid()
plt.xlabel('length of simulation (s)')
plt.title('Simulation results for a network of 10 neurons')
plt.savefig('results_10_neurons.pdf', dpi=300)
plt.show()

plt.figure()
# plt.plot([500,1000,1500], np.mean(mae_10, axis=1), label='MAE')
plt.plot([500,1000,1500], np.mean(acc_20, axis=1), label='accuracy')
plt.plot([500,1000,1500], np.mean(prec_20, axis=1), label='precision')
plt.plot([500,1000,1500], np.mean(rec_20, axis=1), label='recall')
plt.legend()
plt.grid()
plt.xlabel('length of simulation (s)')
plt.title('Simulation results for a network of 20 neurons')
plt.savefig('results_20_neurons.pdf', dpi=300)
plt.show()
