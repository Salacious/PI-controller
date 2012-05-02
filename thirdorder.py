# -*- coding: utf-8 -*-
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
from operator import itemgetter
import pareto
from overshoot import*
from risetime import*
from plotgraphs import*
from response import* 

tfinal = 10
dt = 0.2
t = np.arange(0, tfinal, dt)
entries = len(t)
num = 10
x = np.zeros((entries,num))
k_c = np.zeros(num)
t_i = np.zeros(num)
por = np.zeros(num)
tr = np.zeros(num)
aa = np.random.rand(num,2)
k_c = 100*aa[:, 0]
t_i = 10*aa[:, 1]
# coefficients of the transfer function
A =3
B = 3
C = 2
kp =0.125
SP = 1
a = 0
count = 0

for k in range(0,num):
    kc =k_c[k]
    ti = t_i[k]
    firstrow =[(ti/(kp*kc)*(C + (kp*kc))), (ti/(kp*kc))*B, (ti/(kp*kc))*A, (ti/(kp*kc))] 
    Adot = [firstrow,[-1 ,0,0,0],[0,-1,0,0],[0, 0 ,-1,0]]
    cmat = -1*np.eye(4)
    Amat = np.dot((linalg.inv(Adot)),cmat)
    rootsA = np.array(linalg.eigvals(Amat))
    Bmat = np.dot(linalg.inv(Adot),[[1],[0] ,[0],[0]])
    Xo = -1*np.dot(linalg.inv(Amat),Bmat*SP)
    for i in range(0,entries):
        At = linalg.expm2(Amat*t[i])
        X = np.dot(((linalg.expm2(At))),Xo)
        x[i,k] = X[0]
        if X[0]> 50:
            print 'the system is unstable, overshoot ratio and rise time undefined'
            x[i,k] = None
            break
        
        count = count + 1 

kc = k_c
ti = t_i
x = np.transpose(x)
por = overshoot(x,SP,num,entries)
tr = risetime(x,SP,num,entries,t)
x = np.transpose(x)
fig,ax1,ax2,ax3,line2,goodpoints = plotgraphs(k_c,t_i,tr,por,x,num,tfinal)
fig = response(ax1,ax2,ax3,x,por,tr,kc,ti,goodpoints,line2,tfinal,dt,fig)