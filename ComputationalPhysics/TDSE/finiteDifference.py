import numpy as np
import cmath

def simulate(parameters, V, xValues, psi):
    
    #import necessary values
    dimensions = int(parameters['Discretization'])
    deltaT = float(parameters['deltaT'])
    deltaX = (float(parameters['xMax']) - float(parameters['xMin'])) / dimensions

    # define an identity matrix 
    I = np.matrix(np.identity(dimensions))   

    # Build the solver matrix
    baseMatrix = np.zeros((dimensions,dimensions), dtype = complex)
    for i in range(dimensions):
	    baseMatrix[i,(i - 1) % dimensions] = -1
	    baseMatrix[i,i] = 2
	    baseMatrix[i,(i + 1) % dimensions] = -1

    # if O boundary conditions
    if (parameters['boundaries'] == False):
        baseMatrix[0, :] = 0
        baseMatrix[(dimensions - 1), :] = 0
        baseMatrix[0, 0] = 1
        baseMatrix[(dimensions - 1), (dimensions - 1)] = 1

    B = V + (I + deltaT * 1j / deltaX**2 * baseMatrix)

    for i in range(dimensions - 1):
        psi[i + 1] = np.linalg.solve(B, psi[i])
    
    return psi
