import pandas as pd
import matplotlib.pyplot as plt
from lammpshade.Constructor import *


UNITS_MAPPING = {
            'real': {
                    'mass': r'(g/mol)',
                    'distance': r'($/AA$)',
                    'time': r'(fs)',
                    'energy': r'$(kcal/mol)$',
                    'velocity': r'($\AA$ / fs)',
                    'force': r'$((kcal/mol)/\AA)$',
                    'torque': r'$(kcal/mol)$',
                    'temperature': r'(K)',
                    'pressure': r'(atm)',
                    'dynamic viscosity': r'(P)',
                    'charge': r'm. of e. c.',
                    'dipole': r'(charge \times \AA)$',
                    'electric field': r'$(V/\AA)$',
                    'density': r'($g/cm^\text{dim}$)'
            },
            'metal': {
                    'mass': r'$\frac{\text{g}}{\text{mol}}$',
                    'distance': r'\AA',
                    'time': r'ps',
                    'energy': r'eV',
                    'velocity': r'$\frac{\text{\AA}}{\text{ps}}$',
                    'force': r'$\frac{\text{eV}}{\text{\AA}}$',
                    'torque': r'eV',
                    'temperature': r'K',
                    'pressure': r'bar',
                    'dynamic viscosity': r'P',
                    'charge': r'multiple of electron charge (1.0 is a proton)',
                    'dipole': r'$\text{charge}\times\text{\AA}$',
                    'electric field': r'V/\text{\AA}',
                    'density': r'$\frac{\text{g}}{\text{cm}^\text{dim}}$'
            }}


class GraphMaker:
    """
    A class that represents a graph maker.

    Attributes:
        df (pandas.DataFrame): The DataFrame containing data.
    
    Methods:
        __init__(self, df): Initializes the GraphMaker object.
        process_columns(self): Processes the DataFrame columns based on the provided keywords list.
        plot_graph(self, columns, df=None, x=None, y=None): Plots the graph based on the provided columns, xlabel, and ylabel.
        run(self, keywords_list, mode='display'): Runs the graph maker based on the provided keywords list and mode.
        interactive_mode(self): Enters the interactive mode for the graph maker.
    """

    def __init__(self, df, keywords_list=None):
        """
        Initializes the GraphMaker object.

        Args:
            df (pandas.DataFrame): The DataFrame containing data.
            keywords_list (list, optional): List of keywords. Defaults to None.

        Raises:
            ValueError: If df is empty.

        Returns:
            None
        """
        if df.empty:
            raise ValueError('Data cannot be empty')
        self.df = df
        self.keywords_list = keywords_list

    def process_columns(self):
        """
        Processes the DataFrame columns based on the provided keywords list.

        Args:
            None

        Returns:
            list: A list containing the column names that match the keywords.
        """
        # Find the column names that match the keywords
        if self.keywords_list is None:
            return self.df.columns.tolist()
        else:
            matching_columns = [keyword for keyword in self.keywords_list if keyword in self.df.columns]
            return matching_columns

    def plot_graph(self, columns, df=None, x=None, y=None):
        """
        Plots the graph based on the provided columns, xlabel, and ylabel.

        Args:
            columns (list): A list containing the column names to be plotted.
            df (pd.DataFrame, optional): The dataframe containing the data to be plotted. Defaults to self.thermo_df.
            x (list, optional): The x-values to be plotted. Defaults to None.
            y (list, optional): The y-values to be plotted. Defaults to None.
        """
        fig, ax = plt.subplots()
        if x is not None and y is not None:
            ax.plot(x, y) # pragma: no cover
        else:
            df = df if df is not None else self.df
            if columns != []:
                for column in columns:
                    ax.plot(df['Time'], df[column]) # pragma: no cover
            else:
                for column in df.columns:
                    if column != 'Time':
                        ax.plot(df['Time'], df[column]) # pragma: no cover
        plt.show() # pragma: no cover

    def run(self, mode, keywords_list=[]):
        """
        Run the GraphMaker in the specified mode.

        Parameters:
        - mode (str): The mode in which to run the GraphMaker. Valid values are 'd' for default mode and 'i' for interactive mode.
        - keywords_list (list): Optional list of keywords to filter the data.

        Raises:
        - ValueError: If an invalid mode is provided.

        Returns:
        - None
        """
        self.keywords_list = keywords_list
        columns = self.process_columns()
        if mode.lower().startswith('d'):
            self.plot_graph(columns)
        elif mode.lower().startswith('i'):
            self.interactive_mode()
        else:
            raise ValueError('Invalid mode')

    def interactive_mode(self):
        """
        Enters the interactive mode for the graph maker.
        
        This method allows the user to interactively plot graphs based on the available data.
        The user is provided with information on the plottable keywords and can select the quantities to display and how to plot them.
        The method supports two modes: Display and Combine.
        In Display mode, multiple figures are displayed with each "Time vs. Quantity" data plotted separately.
        In Combine mode, a single figure is displayed with all "Time vs. Quantity" data plotted together.
        The user can exit the program by typing "exit".
        """
        # Give user info on plottable keywords
        print('The following quantities have been found: ' +
              ', '.join(self.df.columns.astype(str))
              )
        
        # Start plotting loop
        while True:
            keyword_check = True
            # Give info on how to plot
            print('Define printing settings:')
            print('Input format: mode [q_name1, q_name2, q_name3]')
            print('To exit the program type: "exit"')
            print('Modes')
            print('Display - Displays a multiple figures with all "Time vs. Quantity" data plotted separately')
            print('Combine - Displays a single figure with all "Time vs. Quantity" data plotted together.')

            # Obtain input by user
            graph_input = input('Select which quantities to display and how: ')
            # Get data from input
            graph_input= graph_input.replace(' ', '').split('[')
            # Get plotting mode
            mode = graph_input[0].lower()

            # Exit the loop
            if mode == 'exit':
                print('Exiting the loop...')
                break

            # Get keywords to plot
            try:
                keywords_list = graph_input[1].replace(']', '').split(',')
            except:
                print('Invalid selection, try again.')
                continue
            # Check if input keywords are plottable
            for keyword in keywords_list:
                if keyword not in list(self.df.columns):
                    print('Error: ' + keyword + ' not found')
                    keyword_check = False
                    
            if keyword_check:
                if mode.lower().startswith('d'):
                    # Plot using display mode
                    for keyword in keywords_list:
                        self.plot_graph([keyword])
                if mode.lower().startswith('c'):
                     # Plot using combine mode
                    self.plot_graph(keywords_list)
            else:
                # If input is invalid, restart the loop
                print('Invalid selection, try again.')
                continue