# -*- coding: utf-8 -*-


def kcfunction(kc,ti,x,entries,t,tfinal,dt,SP):
    import numpy as np
    from operator import itemgetter
   
# calulates the overshoot ratio
    def overshoot():
      
            if np.isnan(x).any()==True:
                por= np.NaN
                tpr = np.NaN
            else:
                por = ((np.max(x))- SP)/SP
                for u in range(0,entries):
                    if x[u] ==np.max(x):
                        tpr = t[u] 
                if por < 0:
                        por = np.NaN
                        tpr= np.NaN
            return {'por':por ,'tpr':tpr}
    por2 = overshoot()
    por = por2['por']
    tpr = por2['tpr']
   
 # calculates the risetime
    def risetime(): 
           
            if np.isnan(x).any():
                tr = np.NaN 
            elif np.isnan(por):
                tr = np.NaN
            
            else:
                for k in range(0, entries-1):    
                    if np.sign(SP - x[k])!=np.sign(SP - x[k+1]):
                        if por ==0:
                            tr1 =np.interp(0.1*SP,[x[k],x[k+1]],[t[k],t[k+1]])
                            tr2 = np.interp(0.9*SP,[x[k],x[k+1]],[t[k],t[k+1]])
                            tr = tr2-tr1
                            break
                        elif por!=0 and np.isnan(por)==False:
                            if np.sign(SP - x[k+1])==0:                 
                                tr = t[k+1]
                            else :
                                tr = np.interp(SP,[x[k],x[k+1]],[t[k],t[k+1]])
                                break
            return tr
    tr= risetime()
    
    return por,tr,tpr
    
