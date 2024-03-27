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
        self.thermo_df = pd.DataFrame(thermo_data, columns=thermo_keywords)
        pass

    def make_graph(self, keywords_list, thermo_df, mode): # pragma: no cover
        #color = []
        #markerstyle = []
        #linestyle = []
        #legend = False
        #grid = False
        gridstyle = '--'
        xlabel = 'Time ' + self.file.get_units('Time')
        if mode == 'display':
            for column in keywords_list:
                if column not in ('Time', 'Step'):
                    fig, ax = plt.subplots()
                    ax.plot(self.thermo_df['Time'], self.thermo_df[column])
                    ax.set_xlabel(xlabel)
                    ax.set_ylabel(ylabel)
                    ax.grid(linestyle=gridstyle)
            plt.show()

        if mode == 'stack':
             fig, ax = plt.subplots()
             for column in keywords_list:
                if column not in ('Time', 'Step'):
                    ax.plot(self.thermo_df['Time'], self.thermo_df[column], label=column)
                    ax.set_xlabel(xlabel)
                    y = column.replace('c_', '').replace('v_', '')
                    ax.grid(linestyle=gridstyle)
             ax.set_xlabel(xlabel)
             ax.legend()
             plt.show()

    def interact_graph(self): # pragma: no cover
        # Give user info on plottable keywords
        print('The following quantities have been found: ' +
              str(self.thermo_df.columns))
        
        # Start plotting loop
        while True:
            keyword_check = True
            # Give info on how to plot
            print('Define printing settings:')
            print('Input format: mode [q_name1, q_name2, q_name3]\n' +
                  'To exit the program type: "exit"')
            print('Modes\n')
            print('Display - Show all the [Time vs. Quantity] graphs separately\n')
            print('Stack - Shows a single [Time vs. Quantities] graph\n')

            # Obtain input by user
            graph_input = input('Select which quantities to display and how:\n')
            # Get data from input
            graph_input= graph_input.replace(' ', '').split('[')
            # Get plotting mode
            mode = graph_input[0].lower()

            # Exit the loop
            if mode == 'exit':
                break

            # Get keywords to plot
            keywords_list = graph_input[1].replace(']', '').split(',')
            # Check if input keywords are plottable
            for keyword in keywords_list:
                if keyword not in list(self.thermo_df.columns):
                            print('Error: ' + keyword + ' not found')
                            keyword_check = False

            if keyword_check:
                if mode.startswith('d'):
                    # Plot using display mode
                    self.make_graph(keywords_list, self.thermo_df, 'display')
                if mode.startswith('s'):
                     # Plot using stack mode
                    self.make_graph(keywords_list, self.thermo_df, 'stack')

            else:
                # If input is invalid, restart the loop
                print('Invalid selection, try again')
        return
