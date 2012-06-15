# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 01:14:09 2012

@author: Conray
"""

import matplotlib.pyplot as plt
from ZN import *
from kcfunction import *
from pymopsocd import *
import simulate
from cohenpid import *
from scipy import linalg
import numpy as np
from plots import *

znset =ZN(simulate.A, simulate.B, simulate.C, simulate.kp)
kczn = znset[0]
tizn = znset[1]

class problemcontrol(problem):
    def __init__(self):
        self.xrange = [(0.1, 3*kczn), (0, 3*tizn)]
	self.bigvalues = array([1.7 , 90])
        self.size = len(self.xrange)
        self.obnames = ['Rise time', 'Overshoot']

    def feasible(self, position):
        A, B = simulate.simulate_matrices(simulate.A, simulate.B, simulate.C, simulate.kp, *position)
        return simulate.stable(A)

    def evaluate(self, position):
	v = simulate.simulate(*position)[1]
        return cevaluation(position, array([v[0], v[2]]))

prob = problemcontrol()
theswarm = swarm(prob, Nparticles=100, 
                         archivesize=50, 
                         maxgen=100,
                         pMut=0.01,
                         rememberevals=True,
                         printinterval=1)
theswarm.run()

plt.figure()
font = {'family' : 'cambria', 
        'weight' : 'normal', 
        'size'   : 14} 
 
plt.matplotlib.rc('font', **font)
plt.figure().set_facecolor('white')
#plt.plot(*zip(*[e.value for e in theswarm.allevals]), color='white', marker='o', linestyle='')
plt.plot(*zip(*sorted([list(e.value) for e in theswarm.archive.list if not isnan(e.value).all()])), color='red',linewidth = 2.5)





tfinal = 100# simulation period
dt = 0.2
t = np.arange(0, tfinal, dt)
entries = len(t)
num =100 # number of tuning constant sets
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
kczn ,tizn,kctl,titl  =ZN(A,B,C,kp) # Ziegler-Nichols settings via function ZN

kccc,ticc = cohenpid(A,B,C,kp)


for k in range(0,num):
    if k==num-2: # Zn settings
        kc = kczn
        ti = tizn
    elif k==num-1:# Cohen Coon settings
        kc = kccc
        ti = ticc
    elif k ==num-3: # Tyreus and Luyben settings
        kc = kctl
        ti = titl
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
plots(kc,ti,x,num,entries,t,tfinal,dt,SP,kcst,tist)

plt.legend(["MOPSO-cd", "Brute Force method"])
plt.xlabel('overshoot' ,fontsize='large')
plt.ylabel('rise time(s)', fontsize = 'large')
plt.show()


