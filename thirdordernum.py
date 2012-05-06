# -*- coding: utf-8 -*-
import numpy as np
from scipy import linalg
from plotgraphs import*
from ZN import*


tfinal = 100
dt = 0.02
t = np.arange(0, tfinal, dt)
entries = len(t)

num = 100
x = np.zeros((entries,num))
k_c = np.zeros(num)
t_i = np.zeros(num)

por = np.zeros(num)
print len(por)
tr = np.zeros(num)
aa = np.random.rand(num,2)

k_c = 10*aa[:, 0]
t_i = aa[:, 1]+0.5
# coefficients of the transfer function
A =3
B = 3
C = 1
kp =0.125
SP = 1
a = 0

# ZN settings
kczn ,tizn  =ZN(A,B,C,kp) # Ziegler-Nichols settings via function ZN

for k in range(0,num):
    state= [0,0,0]
    count = 0
    de = 0
    z= 0
    y = 0
    xt = 0.5
    if k==num-1:
        kc = kczn
        ti = tizn    
    else:    
        kc =k_c[k]
        ti = t_i[k]             
   #Euler integration
    for i in range (0,entries):
            E = SP- state[2]
            m =  kc*(E + de/ti)
            dPdt = [(kp*m) -(C*state[2]) -( B*state[1])- (A*state[0]),state[0],state[1]]
            state = state + np.multiply(dt,dPdt)
            de = de + (E*dt)
            x[i,k] = state[2]
            if state[2] > 2*SP:
                print 'the system is unstable, overshoot ratio and rise time undefined'
                x[:,k] = None
                break
    k_c[k] = kc
    t_i[k] = ti 
        
kc = k_c
ti = t_i
x = x.T
fig = plotgraphs(kc,ti,x,num,entries,t,tfinal,dt,SP)










