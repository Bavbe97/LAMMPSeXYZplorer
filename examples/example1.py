# Example 1: Convert the YAML file to a XYZ file

import lammpshade as lp

# Load the YAML file
sim = lp.Simulation("input_example.yaml")

# Convert the YAML file to a XYZ file
sim.convert_to_xyz("output_example.xyz")
