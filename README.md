![Unit Tests](https://github.com/Bavbe97/LAMMPShade/actions/workflows/unit_test.yml/badge.svg)

# LAMMPShade

LAMMPShade is a toolkit for working with LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator) simulations. It is an open-source library designed to collect useful functions to analyze and convert OUTPUT files and, potentially in the future, generate INPUT files in a fast and efficient way.

In its current state, LAMMPShade is capable of reading YAML-like output, converting them into XYZ files for third-party visualization software, and creating preliminary plots to analyze the data from each step of a LAMMPS molecular dynamics simulation.

## Why LAMMPShade?

At the time of writing this, there is not a satisfactory implementation in Python for efficiently reading YAML files, especially when compared to implementations in other programming languages. Existing Python implementations can be notably slow. However, LAMMPShade fills this gap by providing an extremely fast and efficient way of reading YAML files specifically tailored for LAMMPS outputs.

### Key Features

- **Fast YAML Reading**: LAMMPShade offers significantly improved performance in reading YAML-like output files compared to existing Python implementations.
- **XYZ File Conversion**: Convert output files to XYZ format for seamless visualization in third-party software.
- **Preliminary Data Analysis**: Generate preliminary plots to analyze data from each step of a LAMMPS molecular dynamics simulation.

## How LAMMPShade Differs

LAMMPShade is not just another generic YAML reader. It is purpose-built for LAMMPS simulations, offering optimized performance and tailored functionalities to meet the specific needs of LAMMPS users.


# How to Install

You can install the library in two ways:

## 1. Download from GitHub

You can download the repository directly from GitHub. Once downloaded, you can use the library by importing it directly from the repository folder into your Python scripts.

```bash
git clone https://github.com/Bavbe97/LAMMPShade
```

## 2. Install with pip

You can also install the library using pip once you've downloaded the repository. Open your terminal and run:

```bash
pip install /path/to/lammpshade/
```

This will install the library along with its dependencies.

## Dependencies

LAMMPShade is tested and working with Python `3.7`, `3.8`, `3.9`, `3.10`, `3.11` and `3.12`. Functionality with older versions is not guaranteed.

LAMMPShade relies on the following dependencies, which should be properly installed beforehand:

- `pandas` (tested for version `2.2`)
- `matplotlib` (tested for version `3.8`)


# Usage

### Basic Usage

To use LAMMPShade in your Python project, follow these simple steps:

1. **Import the library**: Start by importing the necessary modules from LAMMPShade into your Python script.

    ```python
    import lammpshade as lp
    ```

2. **Initialize a Simulation object**: Create a Simulation object by providing the path to the LAMMPS output file you intend to convert

    ```python
    simulation = lp.Simulation("output.yaml")
    ```

3. **Convert to XYZ**: Convert the output data to XYZ format using the `convert_to_xyz` function.

    ```python
    simulation.convert_to_xyz("output.xyz")
    ```

4. **Plot Graphs**: Initiate an interactive loop in your terminal to visualize various graphs based on the thermo data of your simulation.

    ```python
    simulation.make_graphs(mode='interactive')
    ```

   Follow the instructions provided in your terminal to navigate and visualize the data.
     
### Advanced Usage

For more advanced usage, you can explore additional functionalities provided by LAMMPShade:

- **Retrieve Next Step Data**: If you need to access the data for each step of your simulation in a dictionary format, you can use the get_next_step() method. This method retrieves the data for the subsequent      step each time it's invoked, making it particularly useful within a while loop.
  
  ```python
  while True:
      step_data = simulation.file.get_next_step()
      # Your script logic using step_data
  ```
  
- **Get thermo data**: If you're only interested on getting the thermo data of your simulation in a pandas Dataframe format.

  ```python
  thermo_dataframe = simulation.get_thermodata()
  ```

### Example

Here's a simple example demonstrating how to use LAMMPShade to read a YAML file and convert it to XYZ format:

```python
# Example of how to use the package
import lammpshade as ls

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
```
By following these steps, you can efficiently work with LAMMPS simulation data using LAMMPShade in your Python projects.


# Wiki

The project's wiki is a work in progress and will be updated with more information and documentation.


# Contributing

The project is open to contributions and suggestions. If you have any ideas or encounter any issues, feel free to open an issue or contact the project maintainer.


# External Links

Here are some external links with useful information:

- [LAMMPS webpage](https://www.lammps.org/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
