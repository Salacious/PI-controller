# -*- coding: utf-8 -*-

import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from operator import itemgetter
import pareto
kp = 10
tau = 45
SP = 1
E_0=0
tfinal = 100
dt = 0.02
t = np.arange(0, tfinal, dt)
entries = len(t)
de = 0
num = 150
x = np.zeros((entries,num))
k_c = np.zeros(num)
t_i = np.zeros(num)

por = np.zeros(num)
print len(por)
tr = np.zeros(num)
aa = np.random.rand(num,2)

k_c = 10*aa[:, 0]
t_i = 10*aa[:, 1]

for k in range(0,num):
    count = 0
    xt = 0.5
    kc = k_c[k]
    ti = t_i[k]
    a = [[ti*((1/(kp*kc)) + 1), tau*ti/ (kp*kc)],[-1,0]]
    aac= [[-1, 0],[0, -1]]
    ainv = LA.inv(a)
    A = np.dot(ainv,aac)
    b = [[-1],[0]]
    B = np.dot(ainv,b)
    
    Xsteady = LA.solve(A,B)
    rootsA = LA.eigvals(A)

   
    
    if (np.sign(rootsA[0].real)==np.sign(rootsA[1].real)) and (np.sign(rootsA[0].real) ==-1) and (rootsA[0].imag!=0):
        counter = 0
        print rootsA
        
        for i in range (0,entries):
             E = SP- xt
             mv =   (kc*(E + (de/ti)))
             xdot = ((kp*mv) - xt)/tau
             xt = xt + (xdot*dt)
             de = de + (E*dt)
             x[i,k] = xt
        por[k] = (np.max(np.absolute(x[:,k])))- SP
        trvstore = np.zeros(entries)
        
        for j in range (0,entries-1 ):
           if np.sign(SP - x[j,k])!=np.sign(SP - x[j+1 ,k]):
                
                if np.sign(SP - x[j+1 ,k])==0:
                    trv = t[j+1]
                else :
                    trv = np.interp(SP,[x[j,k],x[j+1,k]],[t[j],t[j+1]])
                trvstore[count] = trv
                count = count + 1
                trv = trvstore[0:count]
                
        tr[k] = np.min(trv)

    else:
        por[k] = None
        tr[k] = None
        x[:,k] = None
kc = k_c
ti = t_i
goodpoints = ~(np.isnan(tr) | np.isnan(por))
idx = np.arange(0,num)
tr = tr[goodpoints]
por = por[goodpoints]
idx = idx[goodpoints]
x = np.transpose(x)[goodpoints]
p = pareto.domset([itemgetter(1), itemgetter(2)], zip(idx, por, tr))
front = p.data
idx, xd, yd = map(np.array, zip(*front))

sortidx = np.argsort(xd)
xd = xd[sortidx]
yd = yd[sortidx]
    
fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
line = ax1.plot(kc[~goodpoints], ti[~goodpoints], 'y.',
	 kc[idx], ti[idx], 'ro')
line1, = ax1.plot(kc[goodpoints], ti[goodpoints], 'b.')
plt.xlabel(r'$K_C$')
plt.ylabel(r'$\tau_I$')
ax2= fig.add_subplot(2,2,2)
line2, =ax2.plot(por, tr, 'o',picker = 5)
line22 = ax2.plot(xd, yd, 'ro-')
plt.axis([0,1, 0,40])
plt.ylabel('risetime')
plt.xlabel('overshoot')
ax3 = fig.add_subplot(2,1,2)
ax3.text(0.02,0.5,'Click on the overshoot vs risetime plot to obtain the time response',fontsize = 13,color = 'red')
plt.ylabel('output')
plt.xlabel('time')
plt.axis([0,tfinal, 0,2])
class timeresponse:
    def __init__(self):
        self.lastind = 0
        self.selected,  = ax2.plot([por[0]], [tr[0]], 'o', ms=12, alpha=0.4,
                                      color='yellow', visible=False)
        self.correspond, = ax1.plot([(kc[goodpoints])[0]],[(ti[goodpoints])[0]],'o',ms = 13,alpha = 0.5,color = 'yellow',visible= False)
       
    def onpick(self,event):

        if event.artist!=line2: return True
    
        NW = len(event.ind)
        if not NW: return True
    
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata
        radius = np.hypot(x-por[event.ind], y-tr[event.ind])
        
        minind = radius.argmin()
        pstn = event.ind[minind]
        self.lastind = pstn
        self.update()
    def update(self):
        if self.lastind is None: return
        pstn = self.lastind
        self.selected.set_visible(True)
        self.selected.set_data(por[pstn], tr[pstn])
        self.correspond.set_visible(True)
        self.correspond.set_data([(kc[goodpoints])[pstn]],[(ti[goodpoints])[pstn]])
        t = np.arange(0, tfinal, dt)
        yt = x[pstn]
        ax3.cla()
        ax3.plot(t,yt)
        fig.canvas.draw()
        return True
        
time = timeresponse()
fig.canvas.mpl_connect('pick_event', time.onpick)
plt.show()
