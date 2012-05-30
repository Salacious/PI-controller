# -*- coding: utf-8 -*-
from scipy import linalg
from kcfunction import*
import numpy as np
 # coefficients of the transfer function Gp = kp/(s^3 + As^2 + Bs +C)
A = 3
B = 3
C = 1
kp =0.125 
SP = 1

def simulate_matrices(A, B, C, kp, kc, ti):
    firstrow =[(ti/(kp*kc)*(C + (kp*kc))), (ti/(kp*kc))*B, (ti/(kp*kc))*A, (ti/(kp*kc))] 
    mat = [firstrow,[-1 ,0,0,0],[0,-1,0,0],[0, 0 ,-1,0]]
    Amat = -1*linalg.inv(mat)
    Bmat = np.dot(linalg.inv(mat),[[1],[0] ,[0],[0]])    

    return Amat, Bmat

def stable(A):
    roots = np.array(linalg.eigvals(A))
    return (roots.real < 0).all()

def simulate(kc, ti):
    tfinal = 100
    dt = 0.2
    t = np.arange(0, tfinal, dt)
    entries = len(t)
    x = np.zeros(entries)
    Amat, Bmat = simulate_matrices(A, B, C, kp, kc, ti)
    
    Xo = -1*np.dot(linalg.inv(Amat), Bmat*SP)
  
    if stable(Amat): 
       
        for i in range(0,entries):
            X = np.dot(1 - linalg.expm2(Amat*t[i]), Xo)
            x[i] = X[0]
    else:
        x = np.NaN
        
    x = np.transpose(x)
    ik = kcfunction(kc,ti,x,entries,t,tfinal,dt,SP)   
    return x, ik
    



