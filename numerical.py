# -*- coding: utf-8 -*-

import numpy as np
from numpy import linalg as LA
from plotgraphs import*


kp = 10
tau = 45
SP = 1
E_0=0
tfinal = 100
dt = 0.2
t = np.arange(0, tfinal, dt)
entries = len(t)
num =150
x = np.zeros((entries,num))
k_c = np.zeros(num)
t_i = np.zeros(num)
por = np.zeros(num)
tr = np.zeros(num)
aa = np.random.rand(num,2)
k_c = 10*aa[:, 0]
t_i = 10*aa[:, 1]

for k in range(0,num):
    xt = 0.5
    de = 0
    kc = k_c[k]
    ti = t_i[k]
    a = [[ti*((1/(kp*kc)) + 1), tau*ti/ (kp*kc)],[-1,0]]
    aac= [[-1, 0],[0, -1]]
    ainv = LA.inv(a)
    A = np.dot(ainv,aac)
    b = [[-1],[0]]
    B = np.dot(ainv,b)
    
    Xsteady = LA.solve(A,B)
    rootsA = LA.eigvals(A)
    if (np.sign(rootsA[0].real)==np.sign(rootsA[1].real)) and (np.sign(rootsA[0].real) ==-1) and (rootsA[0].imag!=0):
        counter = 0 
        for i in range (0,entries):
             E = SP- xt
             mv =   (kc*(E + (de/ti)))
             xdot = ((kp*mv) - xt)/tau
             xt = xt  + (xdot*dt)
             de = de + (E*dt)
             x[i,k] = xt
    else:
        por[k] = None
        tr[k] = None
        x[:,k] = None
kc = k_c
ti = t_i
x = np.transpose(x)
fig = plotgraphs(kc,ti,x,num,entries,t,tfinal,dt,SP)

