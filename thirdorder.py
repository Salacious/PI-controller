# -*- coding: utf-8 -*-
import numpy as np
from scipy import linalg
from plotgraphs import *
from ZN import *

tfinal = 100# simulation period
dt = 0.2
t = np.arange(0, tfinal, dt)
entries = len(t)
num =25 # number of tuning constant sets
x = np.zeros((entries,num))
k_c = np.zeros(num)
t_i = np.zeros(num)
por = np.zeros(num)
tr = np.zeros(num)
aa = np.random.rand(num,2)
k_c = (60 - 2)*aa[:, 0] +2
t_i = (16-0)*aa[:, 1] 
# coefficients of the transfer function Gp = kp/(s^3 + As^2 + Bs +C)
A =3
B = 3
C = 1
kp =0.125 
SP = 1
kcst = np.arange(0,60,dt)
# Relatiopnship btwn kc and Ti obtained through the direct substitution method
tist =kp*kcst*A**2/(((A*B) - C - (kp*kcst))*(C + (kp*kcst)))
kczn ,tizn  =ZN(A,B,C,kp) # Ziegler-Nichols settings via function ZN


for k in range(0,num):
    if k==num-1:
        kc = kczn
        ti = tizn
    else:    
        kc =k_c[k]
        ti = t_i[k]
    firstrow =[(ti/(kp*kc)*(C + (kp*kc))), (ti/(kp*kc))*B, (ti/(kp*kc))*A, (ti/(kp*kc))] 
    mat = [firstrow,[-1 ,0,0,0],[0,-1,0,0],[0, 0 ,-1,0]]
    Amat = -1*linalg.inv(mat)
    rootsA = np.array(linalg.eigvals(Amat))
    Bmat = np.dot(linalg.inv(mat),[[1],[0] ,[0],[0]])
    Xo = -1*np.dot(linalg.inv(Amat),Bmat*SP)
   
    if (rootsA.real < 0).all():
        for i in range(0,entries):
            X = np.dot(1 - linalg.expm2(Amat*t[i]), Xo)
            x[i,k] = X[0]
    else:
        x[:,k] = np.NaN
        
    
    k_c[k] = kc
    t_i[k] = ti
kc = k_c
ti = t_i
x = x.T
fig = plotgraphs(kc,ti,x,num,entries,t,tfinal,dt,SP,kcst,tist)


