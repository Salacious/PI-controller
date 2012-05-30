# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from ZN import *
from kcfunction import *
from pymopsocd import *
import simulate

kczn, tizn  =ZN(simulate.A, simulate.B, simulate.C, simulate.kp)

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
theswarm = swarm(prob, Nparticles=100, 
                         archivesize=70, 
                         maxgen=200,
                         pMut=0.1,
                         rememberevals=True,
                         printinterval=1)
theswarm.run()

plt.figure()
plt.plot(*zip(*[e.value for e in theswarm.allevals]), color='blue', marker='.', linestyle='')
plt.plot(*zip(*sorted([list(e.value) for e in theswarm.archive.list if not isnan(e.value).all()])), color='red')
plt.show()
