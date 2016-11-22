# main.py

import sys
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import cmath
import random
import potentials
import crankNicolson
import finiteDifference
from matplotlib import animation

# optional user input values
params = ['Algorithm', 'Discretization', 'deltaT', 'xMin', 'xMax', 'k0', 
          'boundaries', 'sigma', 'potential', 'V0', 'a', 'b', 'H']
# initial conditions should the user opt to not input anything
initial_vals = ['CrankNicolson', 100, 0.05, -5.0, 5.0, 1.0, True, 200.0, 
                'harmonicOscillator', 0, 0, 0, 0]
parameters = {}

# function that creates the initial x values that will be used by the
# two different algorithms 
def getXs(dimensions):
    dimensions = int(dimensions)
    # import and define the necessary parameters
    xRange = float(parameters['xMax']) - float(parameters['xMin'])
    deltaX = xRange / dimensions
    xShift =  .5 * xRange 
    
    xValues = np.zeros(dimensions) 
    for j in range(0, dimensions):        
        xValues[j] = j * deltaX - xShift 

    return xValues

# Initialzes the matrix where the steps of psi will be stored
def initializePsi(xValues, dimensions):
    dimensions = int(dimensions)

    # import and define the necessary paramters 
    sigma = float(parameters['sigma'])
    k0 = float(parameters['k0'])
    xRange = float(parameters['xMax']) - float(parameters['xMin'])
    deltaX = xRange / dimensions
    
    # for normalization
    area = 0.0 
    psi = np.zeros((dimensions, dimensions), dtype = complex)
    for i in range(dimensions):        
        # this uses the function found in Tim's notebbok
        xVal = float(xValues[i])
        # print(sigma);
        exponent = complex(np.exp(.25 * xVal * (4*i * k0 - xVal * sigma**2)))
        packetXval = exponent * np.sqrt(np.pi) * sigma
        packetXval = packetXval / np.sqrt(np.sqrt(2) * np.pi**(3/2) * sigma)
        psi[0, i] = packetXval
        area += packetXval
    psi = psi / area
    return psi

# animation function
def anim(psi, xValues, V, dimensions):

    # set up plot
    fig = plt.figure()
    ax = plt.axes(xlim=(-5, 5), ylim=(-1, 1))
    psi_x_line, = ax.plot([],[],lw=2)   # fully defeind psi
    psi_xr_line, = ax.plot([],[],lw=1)  # real component 
    psi_xi_line, = ax.plot([],[],lw=1)  # imaginary component

    V_x_line, = ax.plot([],[],lw=3) # potential

    # define initializer
    def init():
        psi_x_line.set_data([],[])  
        psi_xr_line.set_data([],[]) 
        psi_xi_line.set_data([],[])
        V_x_line.set_data([],[])    
        return (psi_x_line, psi_xr_line, psi_xi_line, V_x_line,)

    # define animation function at each frame
    def animate(i):
        x = np.linspace(xValues[0], xValues[dimensions - 1], dimensions)
        y = psi[i]
        yr = psi[i].real
        yi = psi[i].imag
        
        # define lines according to psi matrix
        psi_x_line.set_data(x,y)
        psi_xr_line.set_data(x,yr)
        psi_xi_line.set_data(x,yi)
        
        # define potential line
        v = np.zeros((dimensions), dtype=complex)
        for j in range(dimensions):
            v[j] = V[j,j]
        V_x_line.set_data(x,v)

        return (psi_x_line, psi_xr_line, psi_xi_line, V_x_line)

    anim = animation.FuncAnimation(fig, animate, init_func = init, 
                                   frames = dimensions, interval = 20)
    plt.show()

def main():
    paramvals = []

    # gather initialization data from user
    for arg in sys.argv:
        paramvals.append(arg)

    paramvals.pop(0) # removes the function name   

    for i in range(len(paramvals)):
        parameters[params[i]] = paramvals[i]
    
    for j in range(len(paramvals), len(params)):
        parameters[params[j]] = initial_vals[j]

    #create a potential function
    Vfun = potentials.potential(parameters['potential'], parameters['a'],
                             parameters['b'], parameters['V0'],
                             parameters['H'])
    dimensions = int(parameters['Discretization'])
    
    # create initial psi and x values
    xValues = getXs(dimensions)
    psi = initializePsi(xValues, dimensions)

    # Build the potential matrix
    V = np.zeros((dimensions, dimensions))
    for i in range(dimensions):
	    V[i,i] = Vfun.potential(xValues[i])

    # call the simulation
    if (parameters['Algorithm'] == 'CrankNicolson') :
        psi = crankNicolson.simulate(parameters, V, xValues, psi)
    else :
        psi = finiteDifference.simulate(parameters, V, xValues, psi) 

    # call animation function
    anim(psi, xValues, V, dimensions)

    quit() 

main()
