import lammpshade as ls

# Example of how to use the package

# The input file is a yaml file that contains the simulation parameters
input = './examples/input_example.yaml'

# The output file is the name of the file that will be created
output = './examples/xyz_example.xyz'

# The mode can be 'interactive' or 'combine'
mode = 'interactive'

# Create a simulation object
sim = ls.Simulation(input)

# Convert the simulation data to xyz format
sim.convert_to_xyz(output)

# Get the thermo data from the simulation
thermo = sim.get_thermodata()

# Create graphs based on the thermo data in an interactive mode
sim.make_graphs(mode)
