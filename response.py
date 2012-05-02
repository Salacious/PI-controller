# -*- coding: utf-8 -*-





def response(ax1,ax2,ax3,x,por,tr,kc,ti,goodpoints,line2,tfinal,dt,fig):
    import numpy as np
    import matplotlib.pyplot as plt
    from operator import itemgetter
    import pareto
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
    return fig

