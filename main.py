# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:18:27 2024

@author: fbarb
"""
import functions.LAMMPSreader as reader


file_path = './examples/input_example.yaml'
output = 'dump_file.xyz'
step = {}

if __name__ == "__main__":
    with open(file_path, 'r') as file:
        reader.read_yaml(file, step)
        