![Unit Tests](https://github.com/Bavbe97/LAMMPShade/actions/workflows/unit_test.yml/badge.svg)
# LAMMPShade

LAMMPShade is a toolkit for working with LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator) simulations. It is an open-source library designed to collect useful functions to analyze and convert OUTPUT files and, potentially in the future, generate INPUT files in a fast and efficient way.

In its current state, LAMMPShade is capable of reading YAML-like output, converting them into XYZ files for third-party visualization software, and creating preliminary plots to analyze the data from each step of a LAMMPS molecular dynamics simulation.

## How to Install

To use LAMMPShade, you can download the repository and use it as a simple Python package. Testing and evaluation of more modules are still ongoing, and once completed, the package will be uploaded to PyPI for easier installation.

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