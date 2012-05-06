# -*- coding: utf-8 -*-
# accept x matrix(num,entries) where entries : values from one set of tuning consts


def plotgraphs(kc,ti,x,num,entries,t,tfinal,dt,SP):
    import numpy as np
    import matplotlib.pyplot as plt
    from operator import itemgetter
    import pareto

# calulates the overshoot ratio
    por = np.zeros(num)
    
    for u in range(0,num):
        if (x[:][u]== None):
            por[u]= None
        else:
            por[u] = ((np.max(np.absolute(x[:][u])))- SP)/SP
# calculates the risetime
    tr = np.zeros(num)
    for j in range(0,num):
        trv = 0
        if (np.isnan(x[j][:])).all()== True:
            tr[j] = None  
        else:
            count = 0
            trvstore = np.zeros(entries)
            for k in range (0,entries-1 ):
                if np.sign(SP - x[j][k])!=np.sign(SP - x[j][k+1]):
                    if np.sign(SP - x[j][k+1])==0:
                        trv = t[k+1]
                    else :
                        trv = np.interp(SP,[x[j][k],x[j][k+1]],[t[k],t[k+1]])
                    trvstore[count] = trv
                    count = count + 1
                    trv = trvstore[0:count]   
                tr[j] = np.min(trv)   
   
# plots the graphs
    
    goodpoints = ~(np.isnan(tr) | np.isnan(por))
    idx = np.arange(0,num)
    tr = tr[goodpoints]
    por = por[goodpoints]
    idx = idx[goodpoints]
    x = x[goodpoints]
    zns = len(por)
    print zns
    p = pareto.domset([itemgetter(1), itemgetter(2)], zip(idx, por, tr))
    front = p.data
    idx, xd, yd = map(np.array, zip(*front))
    print por[zns-1]
    print tr[zns-1]
    sortidx = np.argsort(xd)
    xd = xd[sortidx]
    yd = yd[sortidx]  
    fig = plt.figure()
    ax1 = fig.add_subplot(2,2,1)
    line = ax1.plot(kc[~goodpoints], ti[~goodpoints], 'y.',
    	 kc[idx], ti[idx], 'ro',kc[num-1],ti[num-1],'ks')
    line1, = ax1.plot(kc[goodpoints], ti[goodpoints], 'b.')
    plt.xlabel(r'$K_C$')
    plt.ylabel(r'$\tau_I$')
    ax2= fig.add_subplot(2,2,2)
    line2, =ax2.plot(por, tr, 'o',picker = 5,)
    line22 = ax2.plot(por[zns-1],tr[zns-1],'ks',xd, yd, 'ro-')
    plt.axis([0,1, 0,40])
    plt.ylabel('risetime')
    plt.xlabel('overshoot')
    ax3 = fig.add_subplot(2,1,2)
    ax3.text(0.02,0.5,'Click on the overshoot vs risetime plot to obtain the time response',fontsize = 13,color = 'red')
    plt.ylabel('output')
    plt.xlabel('time')
    plt.axis([0,tfinal, 0,2])
        
# graphs interaction 
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
    



