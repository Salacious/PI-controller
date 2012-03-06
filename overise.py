# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import math
SP = 1

def outp(kc,ti):
    t = np.linspace(0,100)
    kp = 10
    tau = 45
    taup = (ti*tau/(kp*kc))**0.5
    damp = ((kp*kc*ti) + ti)/(2*kp*kc*taup)
    if (damp >0 and  damp<1):
        A = SP
        phi = math.acos(damp)
        tr= (np.pi - phi)*taup/(math.sin(phi))
        por = math.e**(-np.pi*math.cos(phi))
        plt.hold(True)
        plt.plot(por,tr,'o') 
        a = math.sqrt(1 - damp**2)
        b = math.e**((-damp/taup)*t)/math.sqrt(a)
        r = (math.sqrt(a)/taup)
        y = r*t + phi
        c = np.sin(y)
        x = A - (b*c)
        return x, tr, por
               
for i in range (0,1000):
    aa = (np.random.rand(1,2))
    x = outp(( 4*aa[0,0]),(5*aa[0,1]))
plt.axis([0,1, 0,40])
plt.ylabel('risetime')
plt.xlabel('overshoot')
plt.show()
    



        
  
#plt.show()












