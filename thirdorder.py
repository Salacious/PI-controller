# -*- coding: utf-8 -*-
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt


tfinal = 100
dt = 0.2
t = np.arange(0, tfinal, dt)
entries = len(t)

num = 1
x = np.zeros((entries,num))
k_c = np.zeros(num)
t_i = np.zeros(num)

por = np.zeros(num)
print len(por)
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
# ZN settings
kczn = 25.57
tizn = 3.02
for k in range(0,num):
    state= [0,0,0.5]
    count = 0
    de = 0
    z= 0
    y = 0
    xt = 0.5
    if k==num-1:
        kc = kczn
        ti = tizn    
    else:    
        kc =k_c[k]
        ti = t_i[k]
    # Stability Check: State space form
    eq =[(ti/(kp*kc)*(C + (kp*kc))), (ti/(kp*kc))*B, (ti/(kp*kc))*A, (ti/(kp*kc))] 
    Adot = [eq,[-1 ,0,0,0],[0,-1,0,0],[0, 0 ,-1,0]]
    cmat = -1*np.eye(4)
    Amat = np.dot(LA.inv(Adot),cmat)
    rootsA = np.array(LA.eigvals(Amat))
    R = np.sign(rootsA.real)
    I = np.sign(rootsA.imag)
                
    if ((R==-1).all()== True):
        print rootsA
    #Euler integration
        for i in range (0,entries):
                E = SP- state[2]
                m =0.3+ kc*(E + de/ti)
                dPdt = [(kp*m) -(C*state[2]) -( B*state[1])- (A*state[0]),state[0],state[1]]
                state = state + np.multiply(dt,dPdt)
                de = de + (E*dt)
                x[i,k] = state[2]
               
        plt.plot(t,x)
        
        por[k] = (np.max(np.absolute(x[:,k])))- SP
        trvstore = np.zeros(entries)
            
#        for j in range (0,entries-1 ):
#           if np.sign(SP - x[j,k])!=np.sign(SP - x[j+1 ,k]):
#                
#                if np.sign(SP - x[j+1 ,k])==0:
#                    trv = t[j+1]
#                else :
#                    trv = np.interp(SP,[x[j,k],x[j+1,k]],[t[j],t[j+1]])
#                trvstore[count] = trv
#                count = count + 1
#                trv = trvstore[0:count]    
##        tr[k] = np.min(trv)
#        a= a+1     
        
    else:
        por[k] = None
        tr[k] = None
        x[:,k] = None

        
plt.show()












