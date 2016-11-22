Time Dependent Schrodinger Equation
Computational Physics 
Project 6
April 13, 2015
Amel Derras, Julia Fowler, John Merfeld, Julia Rowe


This fun pile of files might look like a mess! But never fear! Everything is 
imported into one final function -- main.py. It is preset to run a harmonic 
oscillator, but it can be changed to run either algorithm with many boundary 
conditions and potentials to choose from--with the code outlined in other 
functions.

The main function can take up to 13 arguments in the following exact order: 
    Algorithm - defaulted to CrankNicolson, any other input causes Finite
                Difference to run
    Discretization - the number of points the x's (and therefore the psi's)
                     will be broken into. 
    deltaT - the size of the time step.  Best when this is less than
             (xMax - xMin) / Discretization
    xMin - the minimum x value. (please input as a decimal)
    xMax - the maximum x value.  (please input as a decimal)
        NOTE: the animation function has our defaulted values hard coded in, 
              so you would likely want to change those for better visualization
    k0 - the initial momentum (please input as a decimal)
    boundaries - a boolean value.  True leads to periodic boundary conditions,
                 False means 0 boundary conditions.
    sigma - the uncertainty in momentum.  (please input as a decimal)
    potential - imported as a string.  The options are: freeWavepacket,
                infiniteSquareWell, harmonicOscillator, triangularSquareWell,
                finiteBarrier, Kronig-Penney, piecewise#1, piecewise#2

    The following parameters are used to create the potential function and 
    only necessary for some of the potentials.   
    V0 - provide for: finiteBarrier, Kronig-Penney, piecewise#1, and piecewise#2
        gives the potential outside the barrier or inside the well. 
        Or the boundary conditions for the two piecewise potentials
    a - provide for: infiniteSquareWell, triangularSquareWell, finiteBarrier, 
        and finiteWelll
        defines the boundary condition
    b - provide for: infiniteSquareWell, finiteBarrier, and finiteWelll
        defines the boundary condition
    H - provide for: finiteBarrier and finiteWell
        defines the the height of the barrier or the potential outside the well

We also got very close to visualizing the Eigen States, and that code is in 
eigenFriends.py.

Enjoy your time.

- Julia, Julia, John, and Amel