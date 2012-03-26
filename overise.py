# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from operator import itemgetter
import pareto

SP = 1
stop = 100
kp = 10
tau = 45
def outp(kc,ti):
    t = np.linspace(0,stop,200)
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
x = np.zeros((N,200))
por = np.zeros(N)
tr = np.zeros(N)
aa = np.random.rand(N,2)
kc = 10*aa[:, 0]
ti = 10*aa[:, 1]

for i in range (0, N):
    x[i,:], tr[i], por[i] = outp(kc[i], ti[i])

goodpoints = ~(np.isnan(tr) | np.isnan(por))
idx = np.arange(0, N)
tr = tr[goodpoints]
por = por[goodpoints]
idx = idx[goodpoints]
x = x[goodpoints]

p = pareto.domset([itemgetter(1), itemgetter(2)], zip(idx, por, tr))
front = p.data
idx, xd, yd = map(np.array, zip(*front))

sortidx = np.argsort(xd)
xd = xd[sortidx]
yd = yd[sortidx]
fig = plt.figure()
#plt.hold(True)
ax1 = fig.add_subplot(2,2,1)
line = ax1.plot(kc[~goodpoints], ti[~goodpoints], 'y.',
	 kc[idx], ti[idx], 'ro')
line1, = ax1.plot(kc[goodpoints], ti[goodpoints], 'b.')
kcst = np.linspace(1.3,10)
tauist = 4*kp*kcst/((1 + kp*kcst)**2/tau)
ax1.plot(kcst,tauist)
#plt.hold(False)
plt.xlabel(r'$K_C$')
plt.ylabel(r'$\tau_I$')
ax2= fig.add_subplot(2,2,2)
#plt.hold(True)
line2, =ax2.plot(por, tr, 'o',picker = 5)
line22 = ax2.plot(xd, yd, 'ro-')
plt.axis([0,1, 0,40])
plt.ylabel('risetime')
plt.xlabel('overshoot')
#plt.hold(False)
ax3 = fig.add_subplot(2,1,2)
ax3.text(0.02,0.5,'Click on the overshoot vs risetime plot to obtain the time response',fontsize = 13,color = 'red')
plt.ylabel('output')
plt.xlabel('time')
class timeresponse:
    def __init__(self):
        self.lastind = 0
        self.selected,  = ax2.plot([por[0]], [tr[0]], 'o', ms=12, alpha=0.4,
                                      color='yellow', visible=False)
       
    def onpick(self,event):

        if event.artist!=line2: return True
    
        NW = len(event.ind)
        if not NW: return True
    
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata
        radius = np.hypot(x-por[event.ind], y-tr[event.ind])
        
        minind = radius.argmin()
        print minind
        pstn = event.ind[minind]
        self.lastind = pstn
        self.update()
    def update(self):
        if self.lastind is None: return
        pstn = self.lastind
        self.selected.set_visible(True)
        self.selected.set_data(por[pstn], tr[pstn])
        t = np.linspace(0,stop,200)
        yt = x[pstn]
        ax3.cla()
        ax3.plot(t,yt)
        return True
        ax1.plot([(kc[goodpoints])[pstn]],[(ti[goodpoints])[pstn]],'o',ms = 13,alpha = 0.5,color = 'yellow',visible= True)
        fig.canvas.draw()
        
time = timeresponse()
fig.canvas.mpl_connect('pick_event', time.onpick)
plt.show()

