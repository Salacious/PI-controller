# -*- coding: utf-8 -*-
# accept x matrix(num,entries) where entries : values from one set of tuning consts

def plotgraphs(kc,ti,x,num,entries,t,tfinal,dt,SP,kcst,tist):
    import numpy as np
    import matplotlib.pyplot as plt
    from operator import itemgetter
    import pareto
# calulates the overshoot ratio
    def overshoot(x,num,SP,entries,t):
        tpr = np.zeros(num)
        por = np.zeros(num)
        for u in range(0,num):
            if (x[:][u]== None):
                por[u]= None
                tpr[u] = None
            else:
                por[u] = ((np.max(x[:][u]))- SP)/SP
                for g in range(0,entries):
                    if x[u][g] ==np.max(x[:][u]):
                        tpr[u] = t[g]
                       
                    if por[u] < 0:
                        por[u] = np.NINF
                        tpr[u] = np.NINF
        return {'por':por ,'tpr':tpr}
    por2 = overshoot(x,num,SP,entries,t)
    por = por2['por']
    tpr = por2['tpr']
    print por
 # calculates the risetime
    def risetime(x,num,entries,SP,t): 
        tr = np.zeros(num)
        for j in range(0,num):
            if (np.isnan(x[j][:])).all()== True:
                tr[j] = None 
            else:
                for k in range(0, entries-1):    
                    if np.sign(SP - x[j][k])!=np.sign(SP - x[j][k+1]): 
                        if np.sign(SP - x[j][k+1])==0:                 
                            tr[j] = t[k+1]
                        else :
                            tr[j] = np.interp(SP,[x[j][k],x[j][k+1]],[t[k],t[k+1]])
                        break
        return tr
    tr= risetime(x,num,entries,SP,t)
    SSoffset = ~np.isneginf(por)
    UNSTABLE =~np.isnan(por) 
    print UNSTABLE          
    

# plots the graphs
    goodpoints = ~(np.isnan(tr)| np.isnan(por)|np.isneginf(por))
    idx = np.arange(0,num)
    tr = tr[goodpoints]
    por = por[goodpoints]
    tpr = tpr[goodpoints]
    idx = idx[goodpoints]
    x = x[goodpoints]
    zns = len(por)
    print len(kc[goodpoints])
    p = pareto.domset([itemgetter(1), itemgetter(2)], zip(idx, por, tr))
    front = p.data
    idx, xd, yd = map(np.array, zip(*front))
    sortidx = np.argsort(xd)
    xd = xd[sortidx]
    yd = yd[sortidx]  
    fig = plt.figure()
    
    ax1 = fig.add_subplot(2,2,1)
    if len(kc[goodpoints])!=len(kc):
        line_a = ax1.plot(kc[~UNSTABLE],ti[~UNSTABLE], 'y.')
        line_c=ax1.plot(kc[~SSoffset],ti[~SSoffset],'k.')
    line_b = ax1.plot(kcst,tist,'k-',kc[idx], ti[idx], 'ro',kc[num-1],ti[num-1],'ks')
  
        
    line1, = ax1.plot(kc[goodpoints], ti[goodpoints], 'b.',picker = 5,)
    plt.xlabel(r'$K_C$')
    plt.ylabel(r'$\tau_I$')
    ax2= fig.add_subplot(2,2,2)
    line2, =ax2.plot(por, tr, 'o',picker = 5,)
    line22 = ax2.plot(por[zns-1],tr[zns-1],'ks',xd, yd, 'ro-')
    plt.axis([-0.2,1, 0,40])
    plt.ylabel('risetime')
    plt.xlabel('overshoot')
    ax3 = fig.add_subplot(2,1,2)
    ax3.text(0.02,0.5,'Click on the overshoot vs risetime plot to obtain the time response',fontsize = 13,color = 'red')
    plt.ylabel('output')
    plt.xlabel('time')
    plt.axis([0,tfinal, 0,2])    
# graphical interaction 
    class timeresponse:
        def __init__(self):
            self.lastind = 0
            
            self.selected,  = ax2.plot([por[0]], [tr[0]], 'o', ms=12, alpha=0.4,
                                          color='yellow', visible=False)
            self.correspond, = ax1.plot([(kc[goodpoints])[0]],[(ti[goodpoints])[0]],'o',ms = 13,alpha = 0.5,color = 'yellow',visible= False)
            
        def onpick(self,event):
    
            if event.artist!=line2:
                self.correspond.set_visible(False)
                self.selected.set_visible(False)
                return True
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
            ax3.plot(t,yt,tpr[pstn],((por[pstn] + 1)*SP),'ro')
            ax3.axhline(y=SP,color = 'r')
            ax3.axvline(x=tr[pstn],ymin=0,ymax = tr[pstn],color='k')
            fig.canvas.draw()
            return True
            
    time = timeresponse()
    fig.canvas.mpl_connect('pick_event', time.onpick)
    
    
    class kctiinteract(timeresponse):
          def __init__(self):
              self.l2 = 0
              self.selectedtc, = ax1.plot([(kc[goodpoints])[0]],[(ti[goodpoints])[0]],'o',ms = 13,alpha = 0.5,color = 'pink',visible= False)
              self.correspondtc,=ax2.plot([por[0]], [tr[0]], 'o', ms=12, alpha=0.4,
                                          color='pink', visible=False)
          def onpick(self,event):
              if event.artist!=line1:
                  self.correspondtc.set_visible(False)
                  self.selectedtc.set_visible(False)                  
                  return True
              NW2 = len(event.ind)
              if not NW2: return True
              x = event.mouseevent.xdata
              y = event.mouseevent.ydata
              r2 = np.hypot(x-(kc[goodpoints])[event.ind], y-(ti[goodpoints])[event.ind])
              m2 = r2.argmin()
              p2 = event.ind[m2]
              self.l2 = p2
              self.update()
          def update(self):
            if self.l2 is None: return
            p2 = self.l2
            self.selectedtc.set_visible(True)
            self.selectedtc.set_data([(kc[goodpoints])[p2]],[(ti[goodpoints])[p2]])
            self.correspondtc.set_visible(True)
            self.correspondtc.set_data(por[p2], tr[p2])
            t = np.arange(0, tfinal, dt)
            yt = x[p2]
            ax3.cla()
            ax3.plot(t,yt,tpr[p2],((por[p2] + 1)*SP),'ro')
            ax3.axhline(y=SP,color = 'r')
         
            fig.canvas.draw()
            return True
    tim = kctiinteract()
    fig.canvas.mpl_connect('pick_event', tim.onpick)
    plt.show()

