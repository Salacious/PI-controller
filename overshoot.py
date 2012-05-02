# -*- coding: utf-8 -*-

# accept x matrix(num,entries) where entries : values from one set of tuning consts
def overshoot(x,SP,num,entries):
    import numpy as np
    por = np.zeros(num)
    
    for u in range(0,num):
        if (x[:][u]== None):
            por[u]= None
        else:
            por[u] = ((np.max(np.absolute(x[:][u])))- SP)/SP
    return por
    


