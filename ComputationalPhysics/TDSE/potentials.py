#potentials.py
#by: Julia Rowe
#for TDSE using discrete algorithms
#last modified: 4/6/15

import math

class potential:
    # takes a string defining the potential and uses case
    # statements to define the potentials. The item returned
    # .potential is a function of x.
	def __init__(self, pot, a, b, L, H):
		a = float(a) #boundary condition 
		b = float(b) #boundary condition
		L = float(L) #Vo
		H = float(H) #barrier height
		if pot == 'freeWavepacket':
			self.potential = lambda x: 0
		elif pot == 'infiniteSquareWell':
			self.potential = lambda x: float('Inf') if ((x < a) or (x > b)) else L
		elif pot == 'harmonicOscillator':
			self.potential = lambda x: .5 * x**2
		elif pot == 'triangularSquareWell':
			self.potential = lambda x: float('Inf') if (x < a) else b
		elif pot == 'finiteBarrier':
			self.potential = lambda x: L if ((x < a) or (x > b)) else H
		elif pot == 'finiteWell':
			self.potential = lambda x: H if ((x < a) or (x > b)) else L
		elif pot == 'Kronig-Penney':
			self.potential = lambda x: L if ((x % (b-a)) <= .5 * (b-a)) else H
		elif pot == 'piecewise#1':
			self.potential = lambda x: x * 1j if ((-L < x) or (x < L)) else float('Inf')
		elif pot == 'piecewise#2':
			self.potential = lambda x: x + x * 1j if ((-L < x) or (x < L)) else float('Inf')
