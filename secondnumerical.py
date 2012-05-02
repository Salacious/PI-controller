# -*- coding: utf-8 -*-



import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

tfinal = 50
dt = 0.2
t = np.arange(0, tfinal, dt)
entries = len(t)
E = 0

kp = 10
tau = 5
damp = 0.303


SP = 1
num = 10
x = np.zeros((entries,num))
k_c = np.zeros(num)
t_i = np.zeros(num)
aa = np.random.rand(num,2)
k_c = 80*aa[:, 0]
t_i = 10*aa[:, 1]
y = 0;
for k in range(0,num):
    de = 0
    xt = 0.5
    ydot1 = 0
    dxdt = 0
    kc = k_c[k]
    ti = t_i[k]
    if kc > (-2*damp*ti)/((2*damp*ti*kp)- (kp*tau)):
        print 'a'

        for i in range (0,entries):
            E = SP- xt
            m = kc*(E + de/ti)
            ydot2 = (kp*m-xt-(2*damp*tau*y))/tau**2
#           
            y = y +(ydot2 *dt)
            xt= xt + (y * dt)
            de = de + (E*dt)
#            print de
            x[i,k] = xt
            print x
            ydot1 = ydot2
        plt.plot(t,x)
    else:
        x = None
plt.show()

