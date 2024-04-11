# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:18:27 2024

@author: fbarb
"""

import lammpshade as ls

sim = ls.Simulation('./examples/input_example.yaml')
sim.convert_to_xyz('./examples/xyz_example.xyz')
thermo = sim.get_thermodata()
sim.make_graphs(mode = 'interactive')