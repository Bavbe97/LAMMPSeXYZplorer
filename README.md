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

## How to Install

You can install the library in two ways:

### 1. Download from GitHub

You can download the repository directly from GitHub. Once downloaded, you can use the library by importing it directly from the repository folder into your Python scripts.

```git clone https://github.com/Bavbe97/LAMMPShade```

### 2. Install with pip

You can also install the library using pip once you've downloaded the repository. Navigate to the root folder of the downloaded repository and run:

```pip install .```

This will install the library along with its dependencies.

## Dependencies

LAMMPShade is tested and working with Python `3.7`, `3.8`, `3.9`, `3.10`, `3.11` and `3.12`. Functionality with older versions is not guaranteed.

LAMMPShade relies on the following dependencies, which should be properly installed beforehand:

- `pandas` (tested for version `2.2`)
- `matplotlib` (tested for version `3.8`)

## Wiki

The project's wiki is a work in progress and will be updated with more information and documentation.

## Contributing

The project is open to contributions and suggestions. If you have any ideas or encounter any issues, feel free to open an issue or contact the project maintainer.

## External Links

Here are some external links with useful information:

- [LAMMPS webpage](https://www.lammps.org/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
