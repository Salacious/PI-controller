# -*- coding: utf-8 -*-

import numpy as np
from kcfunction import*
from ZN import*
from system import*
from pylab import *

fig =figure()
ax1 = fig.add_subplot(2,2,1)
xlabel(r'$K_C$')
ylabel(r'$\tau_I$')
axis([-0.2,100, 0,40])
ax2= fig.add_subplot(2,2,2)
axis([-0.2,1, 0,150])
ylabel('risetime')
xlabel('overshoot')

ax3 = fig.add_subplot(2,1,2)
ylabel('output')
xlabel('time')
tfinal = 200
dt = 0.2
t = np.arange(0, tfinal, dt)
entries = len(t)
axis([0,tfinal, 0,2])
SP = 1
class kctiinteract():
   event = None
   xdatalist = []
   ydatalist = []
   def mycall(self, event):
      self.event = event
      self.xdatalist.append(event.xdata)
      self.ydatalist.append(event.ydata)
      ax1.hold(True) # overlay plots.
      kc = event.xdata
      ti = event.ydata
        # Plot a red circle where you clicked.
      

      draw()  # to refresh the plot.

      t = np.arange(0, tfinal, dt)
      xw = system(kc,ti)
      x = xw['x']
      kcst = xw['kcst']
      tist = xw['tist']
      ax1.plot(kcst,tist,'k-')
      obj = kcfunction(kc,ti,x,entries,t,tfinal,dt,SP)
      por = obj['por']
      tr = obj['tr']
      tpr = obj['tpr']
      if np.isnan(por)==True:
          ax3.hold(False)
          ax3.cla()
          
          ax3.text(0.02,0.5,'The system is unstable',fontsize = 13,color = 'red')
          ax1.plot([event.xdata],[event.ydata],'k*')
          
      elif np.isneginf(por)==True:
          ax1.hold(True)
          line_c=ax1.plot(kc,ti,'ko')   
      else:
          print por
          print tr
          ax3.cla()
          ax3.hold(True)
          ax2.hold(True)
          ax3.plot(t,x)
          ax1.plot([event.xdata],[event.ydata],'go')
          ax2.plot([por],[tr],'bo')
          
          ax3.plot(tpr,((por + 1)*SP),'ro')
          ax3.axhline(y=SP,color = 'r')
         
      fig.canvas.draw()
      return True
if __name__=="__main__":
#    # Example usage
        mouse = kctiinteract()
        connect('button_press_event', mouse.mycall)
        
        show()










