# Example 3: Get data from each step

import lammpshade as lp

# Load the YAML file
sim = lp.Simulation("input_example.yaml")

# Get next step data from the simulation file
while True:
    step_data = sim.file.get_next_step()
    print(step_data)
