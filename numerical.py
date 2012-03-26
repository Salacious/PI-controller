# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import pareto
Kp = 10
taup = 45
SP = 1
E_0=0
tfinal = 100
dt = 0.2
mv = 0.5
t = np.arange(0, 100, dt)
entries = len(t)
de = 0
x =0.5
#KC = 1
#ti = 5
xt = np.zeros((entries,entries))
N = 100
kc = np.zeros(entries)
ti = np.zeros(entries)

por = np.zeros(entries)
tr = np.zeros(entries)
for k in range(0,entries):
    kc= 10*np.random.rand(1)
    ti = 10*np.random.rand(1)
    
    for i in range (0,entries):
         E = SP- x
         mv = kc*(E + (de/ti))
         xdot = ((Kp*mv) - x)/taup
         x = x + xdot*dt
         de = de + E*dt
         xt[i,k] = x
    por[i] = max(max(xt))
    z = np.array([np.interp(SP,xt,t)])
    tr[i] = min(z)
goodpoints = ~(np.isnan(tr) | np.isnan(por))
idx = np.arange(0, entries)
tr = tr[goodpoints]
por = por[goodpoints]
idx = idx[goodpoints]
xt= xt[goodpoints]
p = pareto.domset([itemgetter(1), itemgetter(2)], zip(idx, por, tr))
front = p.data
idx, xd, yd = map(np.array, zip(*front))

sortidx = np.argsort(xd)
xd = xd[sortidx]
yd = yd[sortidx]
    
plt.subplot(2,2,1)
plt.plot(kc,ti,'o')
plt.xlabel(r'$K_C$')
plt.ylabel(r'$\tau_I$')
plt.subplot(2,2,2)
plt.plot(por,tr,'o')
plt.plot(xd, yd, 'ro-')
plt.ylabel('risetime')
plt.xlabel('overshoot')
plt.show()
    
    
    



