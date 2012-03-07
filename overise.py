# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from operator import itemgetter
import pareto

SP = 1

def outp(kc,ti):
    t = np.linspace(0,100)
    kp = 10
    tau = 45
    taup = (ti*tau/(kp*kc))**0.5
    damp = ((kp*kc*ti) + ti)/(2*kp*kc*taup)
    
    if (damp > 0 and damp < 1):
        A = SP
        phi = math.acos(damp)
        tr= (np.pi - phi)*taup/(math.sin(phi))
        por = math.e**(-np.pi*math.cos(phi))
        a = math.sqrt(1 - damp**2)
        b = math.e**((-damp/taup)*t)/math.sqrt(a)
        r = (math.sqrt(a)/taup)
        y = r*t + phi
        c = np.sin(y)
        x = A - (b*c)
    else:
        x = None
	tr = None
	por = None
	
    return x, tr, por

N = 1000
por = np.zeros(N)
tr = np.zeros(N)
aa = np.random.rand(N,2)
kc = 10*aa[:, 0]
ti = 10*aa[:, 1]

for i in range (0, N):
    x, tr[i], por[i] = outp(kc[i], ti[i])

goodpoints = ~(np.isnan(tr) | np.isnan(por))
idx = np.arange(0, N)
tr = tr[goodpoints]
por = por[goodpoints]
idx = idx[goodpoints]

p = pareto.domset([itemgetter(1), itemgetter(2)], zip(idx, por, tr))
front = p.data
idx, xd, yd = map(np.array, zip(*front))

sortidx = np.argsort(xd)
xd = xd[sortidx]
yd = yd[sortidx]

plt.subplot(1, 2, 1)
plt.plot(kc[goodpoints], ti[goodpoints], 'b.',
	 kc[~goodpoints], ti[~goodpoints], 'y.',
	 kc[idx], ti[idx], 'ro')
plt.xlabel('K_C')
plt.ylabel('tau_I')
plt.subplot(1, 2, 2)
plt.plot(por, tr, '.', xd, yd, 'ro-')

plt.axis([0,1, 0,40])
plt.ylabel('risetime')
plt.xlabel('overshoot')
plt.show()
