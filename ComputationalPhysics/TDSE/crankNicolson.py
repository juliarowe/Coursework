# Implementation of the Crank Nicolson algorithm 

import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

# primary function that is called by main
def simulate(parameters, V,  xValues, psi):
    
    # Get necessary values
    dimensions = int(parameters['Discretization'])
    deltaT = float(parameters['deltaT'])
    
    # Initialize the additional matrices
    A = np.zeros((dimensions, dimensions), dtype = complex)
    I = np.matrix(np.identity(dimensions))  

    # Create the tridiagonal matrix
    for i in range(0, dimensions):
        for j in range(0, dimensions):
            if i == j:
                A[i ,(j-1) % dimensions] = 1
                A[i, j % dimensions] = -2
                A[i, (j+1) % dimensions] = 1
                break
        
    # H is the hamiltonian: see textbook for details
    H = A + V
    Hminus = (I - (1j*deltaT/2)*H)
    Hplus = (I + (1j*deltaT/2)*H)

    # 0 boundary conditions
    if (parameters['boundaries'] == False):
        
        # make the right hand side zero
        Hminus[0] = 0
        Hminus[(dimensions - 1)] = 0
        
        # make the left hand side so first and last rows
        # have the only one element in the row. 
        # psi[0,0] = 0 and psi[last,last] = 0
        Hplus[0] = Hplus[dimensions-1] = 0
        Hplus[0,0] = 1 
        Hplus[-1,-1] = 1

    HminusSparse = csr_matrix(Hminus)
    HplusSparse = csr_matrix(Hplus)

    # Hplus psi[i] = Hminus psi[i + 1]
    for i in range(1, dimensions):
        psi[i] = spsolve(HplusSparse, HminusSparse.dot(psi[i - 1]))   
 
    return psi
