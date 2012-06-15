# -*- coding: utf-8 -*-
import numpy as np
from scipy import linalg
def cohenpid(A,B,C,kp):
    m_t = 0.2
    Astate = [[B,A,1],[-1,0,0],[0,-1,0]]
    Avar = [[-C,0,0],[0,-1,0],[0,0,-1]]
    forcingfunc = [[kp],[0],[0]]
    Amat = np.dot(linalg.inv(Astate),Avar)
    Bmat = np.dot(linalg.inv(Astate),forcingfunc)
    Xo = -1*np.dot(linalg.inv(Amat),Bmat*m_t)
    tfinal = 10# simulation period
    dt = 0.005
    t = np.arange(0, tfinal, dt)
    entries = len(t)
    x = np.zeros((entries,1))
    Astep = m_t
    Bv = kp*Astep
    for i in range(0,entries):
        X = np.dot(1 - linalg.expm2(Amat*t[i]), Xo)
        x[i] = X[0]
    
    t0 = 0
    for j in range(0,entries-1):
        if np.sign(0-x[j])==0:
            t0 = t[j]            
        if np.sign((0.5*Bv) - x[j]) != np.sign((0.5*Bv) -x[j+1]):
            t2 = np.interp(0.5*Bv,[x[j][0],x[j+1][0]],[t[j],t[j+1]])
        if np.sign((0.632*Bv) - x[j]) != np.sign((0.632*Bv) -x[j+1]):
            t3 = np.interp(0.632*Bv,[x[j][0],x[j+1][0]],[t[j],t[j+1]])
    t1 = (t2 - (np.log(2))*t3)/(1 - np.log(2))
    tau = t3-t1
    tdel = t1- t0
    K= Bv/Astep
    r = tdel/tau
    kccc = (1/(r*K))*(0.9 + (r/12))
    ticc = tdel*(30 + (3*r))/(9 + (20*r))
    return kccc,ticc
