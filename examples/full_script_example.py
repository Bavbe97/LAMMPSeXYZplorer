# An useful example of a full script using lammpshade is shown below.

import lammpshade as lp

# Load the YAML file
sim = lp.Simulation("input_example.yaml")

# Convert the YAML file to a XYZ file
sim.convert_to_xyz("output_example.xyz")

# Get the thermo data from the simulation file
sim_dataframe = sim.get_thermodata()

# Print the thermo data
print(sim_dataframe)

# Make graphs from the simulation data
sim.make_graphs(mode='interactive')
