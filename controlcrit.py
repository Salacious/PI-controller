# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from ZN import *
from kcfunction import *
from pymopsocd import *
import simulate

znset =ZN(simulate.A, simulate.B, simulate.C, simulate.kp)
kczn = znset[0]
tizn = znset[1]

class problemcontrol(problem):
    def __init__(self):
        self.xrange = [(0.1, 3*kczn), (0, 3*tizn)]
	self.bigvalues = array([1.7 , 90])
        self.size = len(self.xrange)
        self.obnames = ['Rise time', 'Overshoot']

    def feasible(self, position):
        A, B = simulate.simulate_matrices(simulate.A, simulate.B, simulate.C, simulate.kp, *position)
        return simulate.stable(A)

    def evaluate(self, position):
	v = simulate.simulate(*position)[1]
        return cevaluation(position, array([v[0], v[2]]))

prob = problemcontrol()
theswarm = swarm(prob, Nparticles=50, 
                         archivesize=25, 
                         maxgen=50,
                         pMut=0.1,
                         rememberevals=True,
                         printinterval=1)
theswarm.run()

plt.figure()
font = {'family' : 'cambria', 
        'weight' : 'normal', 
        'size'   : 14} 
 
plt.matplotlib.rc('font', **font)
plt.figure().set_facecolor('white')
plt.plot(*zip(*[e.value for e in theswarm.allevals]), color='white', marker='o', linestyle='')
plt.plot(*zip(*sorted([list(e.value) for e in theswarm.archive.list if not isnan(e.value).all()])), color='red',linewidth = 2.5)
plt.legend(["swarm particles", "Pareto Front"])
plt.xlabel('overshoot' ,fontsize='large')
plt.ylabel('rise time(s)', fontsize = 'large')
plt.show()
