# -*- coding: utf-8 -*-
from system import*

def kcfunction(kc,ti,x,entries,t,tfinal,dt,SP):
    import numpy as np
    from operator import itemgetter
    import pareto
    print x
# calulates the overshoot ratio
    def overshoot(x,entries,SP,t):
      
            if (np.isnan(x)==True).all():
                por= None
                tpr = None
            else:
                por = ((np.max(x))- SP)/SP
                for u in range(0,entries):
                    if x[u] ==np.max(x):
                        tpr = t[u] 
                if por < 0:
                        por = np.NINF
                        tpr= np.NINF
            return {'por':por ,'tpr':tpr}
    por2 = overshoot(x,entries,SP,t)
    por = por2['por']
    tpr = por2['tpr']
   
 # calculates the risetime
    def risetime(x,entries,SP,t,por): 
           
            if (np.isnan(x)==True).all():
                tr = None 
            elif por== np.NINF:
                tr = np.NINF
            else:
                for k in range(0, entries-1):    
                    if np.sign(SP - x[k])!=np.sign(SP - x[k+1]): 
                        if np.sign(SP - x[k+1])==0:                 
                            tr = t[k+1]
                        else :
                            tr = np.interp(SP,[x[k],x[k+1]],[t[k],t[k+1]])
                        break
            return tr
    tr= risetime(x,entries,SP,t,por)
    
    return {'por':por,'tr':tr,'tpr':tpr}
    
#    if por== None:
#        line_a = ax1.plot(kc,ti, 'y.')
#        print 'the sytem is unstable'
#    elif por == np.NINF:
#        line_c=ax1.plot(kc,ti,'k.')
#        print 'The system has a steady state offset'
#    else:
#        line1, = ax1.plot(kc, ti, 'b.',picker = 5,)
#        ax3.plot(t,x)
#        line2, =ax2.plot(por, tr, 'o',picker = 5,)
        

# plots the graphs
#    goodpoints = ~(np.isnan(tr)| np.isnan(por)|np.isneginf(por))
#    idx = np.arange(0,num)
#    tr = tr[goodpoints]
#    por = por[goodpoints]
#    tpr = tpr[goodpoints]
#    idx = idx[goodpoints]
#    x = x[goodpoints]
#    print len(kc[goodpoints])
#    p = pareto.domset([itemgetter(1), itemgetter(2)], zip(idx, por, tr))
#    front = p.data
#    idx, xd, yd = map(np.array, zip(*front))
#    sortidx = np.argsort(xd)
#    xd = xd[sortidx]
#    yd = yd[sortidx]    
#    line_b = ax1.plot(kcst,tist,'k-',kc[idx], ti[idx], 'ro',kc[num-1],ti[num-1],'ks')
  
        
    
    
    
#    line22 = ax2.plot(por[zns-1],tr[zns-1],'ks',xd, yd, 'ro-')
    
       
# graphical interaction  
    
   

