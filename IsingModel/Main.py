from Metropolis import *
from Wolff import *
from SquareLattice import *
from TriangleLattice import *
import json
from multiprocessing import Pool

export_dir = "export/"

# A list of lattice configurations to test
# a configuration is given by a tuple (LatticeType, NumberOfDimensions, Size)
lattices_to_test =[(SquareLattice, 1, 30), (SquareLattice, 2, 30), (SquareLattice, 3, 10), (TriangleLattice, 2, 30)]

# The number of processes for multithreading
number_processes = 7

# The simulation stops after max_num_flips_multiplier*(size^dimensions) flips have been made
max_num_flips_multiplier = 100

# The simulation takes a snapshot every (size^dimensions)/flip_interval_divisor flips
flip_interval_divisor = 10

# Coupling constants to try
js = [-1, 1]

# Different values of k*T to try
kts = [0.1, 0.5, 0.9, 1.3, 1.7, 2.1, 2.5, 2.9, 3.3]

def simulate_ising(((LatticeClass, num_dimensions, size), SimulationClass)):
    # results list holds the results for separate simulations with varying js and kts
    results = []
    num_lattice_points = math.pow(size, num_dimensions)
    max_num_flips = max_num_flips_multiplier * num_lattice_points
    flip_interval = num_lattice_points / flip_interval_divisor
    for j in js:
        for temp in kts:
            lattice = LatticeClass(size, num_dimensions)
            simulation = SimulationClass(lattice, temp, j, flip_interval)
            while simulation.get_num_flips() <= max_num_flips:
                simulation.step()
            results.append(simulation.export())
    export_to = export_dir + SimulationClass.__name__ + "_" + LatticeClass.__name__ + str(num_dimensions) +  ".json"
    with open(export_to, 'w') as outfile:
        json.dump(results, outfile)

if __name__ == '__main__':
    # Do each simulation case in parallel since Wolff is really slow
    p = Pool(processes=number_processes)
    args = []
    for lattice_info in lattices_to_test:
        for SimulationClass in [Metropolis, Wolff]:
            args.append((lattice_info, SimulationClass))
    p.map(simulate_ising, args)