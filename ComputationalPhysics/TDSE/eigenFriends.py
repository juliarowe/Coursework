
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import potentials
import cmath

a = -10.
b = 10.
dim = 500
deltaX = (b - a) / dim
deltaT = 1

# EIGEN STATES?

baseMatrix = np.matrix(np.zeros((dim, dim), dtype=np.complex))

initialValues = np.matrix(np.zeros((dim,1), dtype=np.complex))
for i in range(dim):
	initialValues[i, 0] = cmath.cos(a + i * deltaX)

V = potentials.potential('harmonic oscillator', a, b, 0, 0)


def zeroConditions(dim):	
# Psi(0) = Psi(x) = 1
	baseMatrix[0, 0] = 1
	baseMatrix[dim - 1, dim - 1] = 1


def periodicConditions(dim, val):
# Psi(0) = Psi(x)
	baseMatrix[0, 0] = val
	baseMatrix[dim - 1, dim - 1] = val

 
def makeMatrix(dim, values):
	jMinus = 0
	j = 1
	jPlus = 2
	deltaTerm = deltaT/(deltaX)**2

	for i in range(1, dim - 1):
		baseMatrix[i, jMinus] = -(1J)*deltaTerm
		baseMatrix[i, j] = -(1J)*(1 + 2*deltaTerm + V.potential(values[i, 0]))
		baseMatrix[i, jPlus] = -(1J)*deltaTerm
		jMinus += 1
		j += 1
		jPlus += 1

	return baseMatrix


def dTerms(deltaT, H, nIter):
	tempMatrix = (.5*(1J)*deltaT*H)
	for i in range(dim):
		for j in range(dim):
			H[i,j] = tempMatrix[i,j] + 1
	return H


def HBuilder(deltaT, DPlus, dim):
	iTerm = (-1)*(2J)/(deltaT)
	for i in range(dim):
		for j in range(dim):
			DPlus[i, j] = iTerm*(DPlus[i, j] - 1)
	return DPlus

def normalize(mat):
	sum = 0
	for i in range(dim):
		sum += abs(mat[i, 0])**2
	mat = mat / np.sqrt(sum)
	return mat


def normVecs(mat):
	norms = []
	sum = 0
	for i in range(dim):
		tempVector = mat[i]
		for j in range(dim):
			sum += (tempVector[i])**2
		norms.append(np.sqrt(sum))
	return norms



zeroConditions(dim)

matrix = makeMatrix(dim, initialValues)

deltaPlus = dTerms(deltaT, matrix, dim)
#print deltaPlus

HList = HBuilder(deltaT, deltaPlus, dim)


HList = np.array(HList)
HMatrix = np.matrix(np.zeros((dim,dim), dtype = complex))

for i in range(dim):
	templist = HList[i]
	for j in range(dim):
		HMatrix[i,j] = templist[j]


eigenInfo = la.eig(HMatrix)
eigenVals = eigenInfo[0]
eigenVecs = eigenInfo[1]

print eigenVecs