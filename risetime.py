# -*- coding: utf-8 -*-


def risetime(x,SP,num,entries,t):
    import numpy as np
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
    print tr     
    return tr


