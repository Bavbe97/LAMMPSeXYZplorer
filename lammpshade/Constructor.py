# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:53:03 2024

@author: fbarb
"""
from lammpshade.YAMLReader import *
from lammpshade.XYZWriter import *
import pandas as pd


class Simulation:
    def __init__(self, filename):
        self.file = YAMLReader(filename)
        self.thermo_keywords = None
        self.thermo_data = None

    def convert_to_xyz(self, output):
        i = 0
        self.output = XYZWriter(output)
        while True:
            step = self.file.get_next_step()
            if not step:
                break
            else:
                if self.thermo_data is None:
                    self.thermo_data = []
                    self.thermo_keywords = step['thermo']['keywords']
                    self.thermo_data.append(step['thermo']['data'])
                else:
                    self.thermo_data.append(step['thermo']['data'])
                self.output.write_to_xyz(step)
                print('Step n. ', i, ' processed')
                i += 1
        self.output.close_file()

    def get_thermodata(self):
        i = 0
        if self.thermo_data is None:
            self.thermo_data = []
            while True:
                step = self.file.get_next_step()
                if not step:
                    break
                if self.thermo_keywords is None:
                    self.thermo_keywords = step['thermo']['keywords']
                self.thermo_data.append(step['thermo']['data'])
                print('Step n. ', i, ' processed')
                i += 1
            thermo = pd.DataFrame(self.thermo_data, columns = self.thermo_keywords)
            return thermo

        else:
            thermo = pd.DataFrame(self.thermo_data, columns = self.thermo_keywords)
            return thermo
    