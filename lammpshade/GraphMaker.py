# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:57:05 2024

@author: fbarb
"""
import pandas as pd
import matplotlib.pyplot as plt
from lammpshade.Constructor import *


class GraphMaker:
    def __init__(self, thermo_data, thermo_keywords, YAMLReader):
        self.thermo_data = thermo_data
        self.thermo_keywords = thermo_keywords
        self.file = YAMLReader
        pass

    def make_graph(self):
        thermo_df = pd.DataFrame(self.thermo_data,
                                 columns=self.thermo_keywords)
        #color = []
        #markerstyle = []
        #linestyle = []
        #legend = False
        #grid = False
        gridstyle = '--'
        xlabel = 'Time ' + self.file.get_units('Time')
        for column in thermo_df:
            if column not in ('Time', 'Step'):
                fig, ax = plt.subplots()
                ax.plot(thermo_df['Time'], thermo_df[column])
                ax.set_xlabel(xlabel)
                y = column.replace('c_', '').replace('v_', '')
                ylabel = y + ' ' + self.file.get_units(y.split('_')[0])
                ax.set_ylabel(ylabel)
                ax.grid(linestyle=gridstyle)
                #plt show per salvare eventualmente il file
        plt.show()

    def interact_graph(self):
        print('Define graphs printing settings:')
        print('The following quantities have been found: ' +
              str(self.thermo_keywords)[1:-1])
        while True:
            keyword_check = True
            print('Input format: mode [q_name1, q_name2, q_name3] \n' +
                  'To exit the program type: "exit"')
            graph = input('Select which quantities to display and how:\n')
            prova = graph.replace(' ', '').split('[')
            if prova[0] == 'display':
                keywords_list = prova[1].replace(']', '').split(',')
                for keyword in keywords_list:
                    if keyword not in self.thermo_keywords:
                        print('Error: ' + keyword + ' not found')
                        keyword_check = False
                if keyword_check:
                    self.make_graph(keywords_list, self.thermo_keywords,
                                    self.thermo_data)
            elif graph == 'exit':
                exit
            else:
                print('Invalid selection, try again')
        return
