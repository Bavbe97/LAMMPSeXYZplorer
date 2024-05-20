# Example 4: Generate a dataframe from the thermo data of the simulation

import lammpshade as lp

# Load the YAML file
sim = lp.Simulation("input_example.yaml")

# Get the thermo data from the simulation file
sim_dataframe = sim.get_thermodata()

# Print the thermo data
print(sim_dataframe)
