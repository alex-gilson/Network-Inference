import numpy as np
import matplotlib.pyplot as plt

plt.figure()
t_1 = np.array([57.957583, 222.298764, 1329.343395, 11801.132728])/60
t_2 = np.array([67.423166, 130.494894, 747.371416, 7002.717412])/60
t_4 = np.array([33.141775, 92.523410, 518.528027, 4694.755803])/60
t_8 = np.array([44.936021, 105.205766, 545.531087, 4639.07996])/60
plt.xlabel('number of neurons')
plt.ylabel('time (min)')
plt.grid()
plt.title('Computation time of NetRate')
t_1_plot, = plt.plot([10,20,30,40],t_1, label='1 processor')
t_2_plot, = plt.plot([10,20,30,40],t_2, label='2 processors')
t_4_plot, = plt.plot([10,20,30,40],t_4, label='4 processors')
t_8_plot, = plt.plot([10,20,30,40],t_8, label='8 processors')
plt.legend(handles=[t_1_plot,t_2_plot,t_4_plot,t_8_plot])
plt.show()

