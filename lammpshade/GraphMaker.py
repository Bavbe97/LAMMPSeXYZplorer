import matplotlib.pyplot as plt

# Constants for the units mapping
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
    A class for creating and plotting graphs based on a DataFrame.

    ...

    Attributes
    ----------
    df : pandas.DataFrame
        The DataFrame containing data.
    keywords_list : list
        List of keywords.

    Methods
    -------
    __init__(df, keywords_list=None)
        Initializes the GraphMaker object.
    process_columns()
        Processes the DataFrame columns based on the provided keywords list.
    plot_graph(columns, df=None, x=None, y=None)
        Plots the graph based on the provided columns, xlabel, and ylabel.
    run(mode, keywords_list=[])
        Runs the GraphMaker in the specified mode.
    interactive_mode()
        Enters the interactive mode for the graph maker.
    print_info()
        Prints information about the inputs of the interactive mode.
    check_and_process_input(graph_input)
        Checks and processes the input provided by the user.
    check_keywords(keywords_list)
        Checks if the keywords provided are valid.
    select_graph_mode(mode, keywords_list)
        Selects the graph mode based on the user input.
    """

    def __init__(self, df, keywords_list=None):
        """
        Initializes the GraphMaker object.

        Arguments
        ---------
        df : pandas.DataFrame
            The DataFrame containing data.
        keywords_list : list, optional
            List of keywords. Defaults to None.

        Raises
        ------
        ValueError
            If df is empty.
        """
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError('Data cannot be empty')

        self.df = df  # DataFrame containing data
        self.keywords_list = keywords_list  # List of keywords

    def process_columns(self):
        """
        Processes the DataFrame columns based on the provided keywords list.

        Arguments
        ---------
        None

        Returns
        -------
        matching_columns : list
            A list containing the column names that match the keywords.
        """
        # Find the column names that match the keywords
        if self.keywords_list is None:
            return self.df.columns.tolist()
        else:
            matching_columns = [
                keyword for keyword in self.keywords_list
                if keyword in self.df.columns
            ]
            return matching_columns

    def plot_graph(self, columns, df=None, x=None, y=None):
        """
        Plot a graph based on the given data.

        Arguments
        ---------
        columns : list
            A list of column names to plot. If empty, all columns except 'Time'
            will be plotted.
        df : pandas.DataFrame, optional
            The DataFrame containing the data. If not provided, the instance's
            df attribute will be used.
        x : array-like, optional
            The x-axis values for the plot. Only used if both x and y are
            provided.
        y : array-like, optional
            The y-axis values for the plot. Only used if both x and y are
            provided.

        Returns
        -------
        None
        """
        # Initialize the plot
        fig, ax = plt.subplots()

        if x is not None and y is not None:
            # Plot the graph with the provided x and y values
            ax.plot(x, y)  # pragma: no cover
        else:
            # Plot the graph based on the columns
            df = df if df is not None else self.df
            if columns != []:
                for column in columns:
                    # Plot the data with the specified columns
                    ax.plot(df['Time'], df[column])  # pragma: no cover
            else:
                for column in df.columns:
                    if column != 'Time':
                        # Plot the data with all columns except 'Time'
                        ax.plot(df['Time'], df[column])  # pragma: no cover
        plt.show()  # pragma: no cover

    def run(self, mode, keywords_list=[]):
        """
        Run the GraphMaker in the specified mode.

        Parameters
        ----------
        mode : str
            The mode in which to run the GraphMaker. Valid values are 'd' for
            default mode and 'i' for interactive mode.
        keywords_list : list, optional
            A list of keywords to be used for processing columns. Defaults to
            an empty list.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If an invalid mode is provided.
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
        Runs the interactive mode for the GraphMaker class.
        Allows the user to select quantities to plot and choose the
        plotting mode.

        Returns
        -------
        None
        """

        # Give user info on plottable keywords
        print('The following quantities have been found: ' +
              ', '.join(self.df.columns.astype(str))
              )

        # Start plotting loop
        while True:

            # Initialize variables
            input_check = True  # Check if input is valid
            keyword_check = True  # Check if keywords are plottable

            # Print info on how to plot
            self.print_info()

            # Obtain input by user
            graph_input = input('Select which quantities to display and how: ')

            # Check and process input
            input_check, mode, keywords_list = self.check_and_process_input(
                graph_input)

            # Exit the loop
            if mode == 'exit':
                print('Exiting the loop...')
                break

            # If input is invalid, restart the loop
            if not input_check:
                print('Invalid input, try again.')
                continue
            
            # Check if keywords are valid
            if input_check:
                keyword_check = self.check_keywords(keywords_list)

            # If input keywords are invalid, restart the loop
            if not keyword_check:
                print('Invalid keywords, try again.')
                continue
            
            # If input is valid, run the GraphMaker
            if keyword_check:
                self.select_graph_mode(mode, keywords_list)

            else:
                # If input is invalid, restart the loop
                print('Invalid selection, try again.')
                continue

    def print_info(self):
        """
        Prints information about the inputs of the interactive mode.

        Returns
        -------
        None
        """

        print('Define printing settings:')  # pragma: no cover
        print('Input format: mode [q_name1, q_name2, q_name3]')  # pragma: no cover
        print('To exit the program type: "exit"')  # pragma: no cover
        print('Modes')  # pragma: no cover
        print('Display - Displays a multiple figures with all "Time vs. '  # pragma: no cover
              'Quantity" data plotted separately')  # pragma: no cover
        print('Combine - Displays a single figure with all "Time vs. '  # pragma: no cover
              'Quantity" data plotted together.')  # pragma: no cover

    def check_and_process_input(self, graph_input):
        """
        Check and process the input provided by the user.

        Arguments
        ---------
        graph_input : str
            The input provided by the user.

        Returns
        -------
        input_check : bool
            True if the input is valid, False otherwise.
        mode : str
            The mode in which to run the GraphMaker.
        keywords_list : list
            A list of keywords to be used for processing columns.
        """

        input_check = True

        # Get data from input
        graph_input = graph_input.replace(' ', '').split('[')

        # Get plotting mode
        mode = graph_input[0].lower()

        try:
            keywords_list = graph_input[1].replace(']', '').split(',')
        except ValueError:
            keywords_list = []
            input_check = False
        except IndexError:
            keywords_list = []
            input_check = False

        return input_check, mode, keywords_list

    def check_keywords(self, keywords_list):
        """
        Check if the keywords provided are valid.

        Arguments
        ---------
        keywords_list : list
            A list of keywords to be checked.

        Returns
        -------
        bool
            True if all keywords are valid, False otherwise.
        """

        for keyword in keywords_list:
            if keyword not in self.df.columns:
                return False
        return True

    def select_graph_mode(self, mode, keywords_list):
        """
        Select the graph mode based on the user input.

        Arguments
        ---------
        mode : str
            The mode in which to run the GraphMaker.
        keywords_list : list
            A list of keywords to be used for processing columns.

        Returns
        -------
        None
        """

        if mode.lower().startswith('d'):
            # Plot using display mode
            for keyword in keywords_list:
                self.plot_graph([keyword])
        if mode.lower().startswith('c'):
            # Plot using combine mode
            self.plot_graph(keywords_list)
