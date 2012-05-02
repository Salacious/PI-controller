# -*- coding: utf-8 -*-


def plotgraphs(kc,ti,tr,por,x,num,tfinal):
    import numpy as np
    import matplotlib.pyplot as plt
    from operator import itemgetter
    import pareto
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
    return fig,ax1,ax2,ax3,line2,goodpoints
