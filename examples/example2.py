# Example 2: Make graphs from the simulation data

import lammpshade as lp

# Load the YAML file
sim = lp.Simulation("input_example.yaml")

# Make graphs from the simulation data
# Comment out the mode you don't want to use

# Interactive mode
sim.make_graphs(mode='interactive')

# Display mode
# si.make_graphs(mode='display')
