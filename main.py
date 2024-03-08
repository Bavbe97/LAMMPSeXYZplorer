# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:18:27 2024

@author: fbarb
"""
import pandas as pd
import lammpshade as ls

prova = ls.Simulation('./examples/input_example.yaml')
thermo_data = prova.get_thermodata()
prova.make_graphs(interact = True)