# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:18:27 2024

@author: fbarb
"""
from LAMMPShade import LAMMPS_reader


file_path = './examples/input_example.yaml'
output = 'dump_file.xyz'
step = {}

if __name__ == "__main__":
    with open(file_path, 'r') as file:
        LAMMPS_reader.read_yaml(file, step)
        