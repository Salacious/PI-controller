# -*- coding: utf-8 -*-
from scipy import linalg


def system(k_c,t_i):
    import numpy as np
   
    tfinal = 200
    dt = 0.2
    t = np.arange(0, tfinal, dt)
    entries = len(t)
    x = np.zeros(entries)
#    k_c = np.zeros(num)
#    t_i = np.zeros(num)
    # coefficients of the transfer function Gp = kp/(s^3 + As^2 + Bs +C)
    A =3
    B = 3
    C = 1
    kp =0.125 
    SP = 1
    kcst = np.arange(0,100,dt)
    # Relatiopnship btwn kc and Ti obtained through the direct substitution method
    tist =kp*kcst*A**2/(((A*B) - C - (kp*kcst))*(C + (kp*kcst)))
#    kczn ,tizn  =ZN(A,B,C,kp) # Ziegler-Nichols settings via function ZN
    kc =k_c
    ti = t_i
    firstrow =[(ti/(kp*kc)*(C + (kp*kc))), (ti/(kp*kc))*B, (ti/(kp*kc))*A, (ti/(kp*kc))] 
    mat = [firstrow,[-1 ,0,0,0],[0,-1,0,0],[0, 0 ,-1,0]]
    Amat = -1*linalg.inv(mat)
    rootsA = np.array(linalg.eigvals(Amat))
    Bmat = np.dot(linalg.inv(mat),[[1],[0] ,[0],[0]])
    Xo = -1*np.dot(linalg.inv(Amat),Bmat*SP)
    print rootsA
    R = np.sign(rootsA.real) 
    I = np.sign(rootsA.imag) 
    if ((R==-1).all()== True): 
        print rootsA
        for i in range(0,entries):
            X = np.dot(1 - linalg.expm2(Amat*t[i]), Xo)
            x[i] = X[0]
    else:
        x = None
        
    kc = k_c
    ti = t_i
    x = np.transpose(x)
    
    return {'x':x ,'kcst':kcst,'tist':tist}