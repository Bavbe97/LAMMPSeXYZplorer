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
        self.file = YAMLReader
        self.thermo_df = pd.Dataframe(thermo_data, columns=thermo_keywords)
        pass

    def make_graph(self): # pragma: no cover
        #color = []
        #markerstyle = []
        #linestyle = []
        #legend = False
        #grid = False
        gridstyle = '--'
        xlabel = 'Time ' + self.file.get_units('Time')
        for column in self.thermo_df:
            if column not in ('Time', 'Step'):
                fig, ax = plt.subplots()
                ax.plot(self.thermo_df['Time'], self.thermo_df[column])
                ax.set_xlabel(xlabel)
                y = column.replace('c_', '').replace('v_', '')
                ylabel = y + ' ' + self.file.get_units(y.split('_')[0])
                ax.set_ylabel(ylabel)
                ax.grid(linestyle=gridstyle)
                #plt show per salvare eventualmente il file
        plt.show()

    def interact_graph(self): # pragma: no cover
        print('The following quantities have been found: ' +
              str(self.thermo_keywords)[1:-1])
        while True:
            keyword_check = True
            print('Define printing settings:')
            print('Input format: mode [q_name1, q_name2, q_name3] \n' +
                  'To exit the program type: "exit"')
            print('Modes\n')
            print('Display - Show all the [Time vs. Quantity] graphs separately\n')
            print('Stack - Shows a single [Time vs. Quantities] graph\n')
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
