from lammpshade.YAMLReader import YAMLReader
from lammpshade.XYZWriter import XYZWriter
from lammpshade.GraphMaker import GraphMaker
import pandas as pd


"""
This module provides a Simulation class for processing LAMMPS simulation data.
"""


class Simulation:
    """
    A class for processing LAMMPS simulation data. The Simulation class reads
    simulation data from a YAML file, converts the data to XYZ format, and
    generates graphs based on the thermo data.

    ...

    Attributes
    ----------
    file : YAMLReader
        The YAMLReader object for reading the simulation data file.
    thermo_keywords : list
        The list of thermo keywords.
    thermo_data : list
        The list of thermo data.
    graphs : GraphMaker
        The GraphMaker object for creating graphs.

    Methods
    -------
    __init__(self, filepath)
        Initializes the Simulation object.
    convert_to_xyz(self, output)
        Converts the simulation data to XYZ format.
    get_thermodata(self)
        Retrieves the thermo data from the simulation data.
    get_step_thermodata(self, step)
        Retrieves the thermo data from the simulation step data.
    make_graphs(self, interact=False)
        Creates graphs from the thermo data.

    """

    def __init__(self, filepath):
        """
        Initializes the Simulation object.

        Parameters
        ----------
        filepath : str
            The path to the simulation data file.

        Raises
        ------
        FileNotFoundError
            If the file is not found.

        """
        self.file = YAMLReader(filepath)  # Create YAMLReader object
        self.thermo_keywords = None  # Thermo keywords of the simulation data
        self.thermo_data = None  # Thermo data of the simulation data

    def convert_to_xyz(self, output, thermo_flag=True):
        """
        Converts the simulation data to XYZ format.

        Parameters
        ----------
        output : str
            The path to the output XYZ file.
        thermo_flag : bool
            A boolean indicating if thermo data should be included.
            Default is True.

        Returns
        ------
        None
        """
        i = 0  # Counter for the number of steps processed

        # Create XYZWriter object
        self.output = XYZWriter(output)
        with self.output as out:
            while True:
                # Get the next step
                step = self.file.get_next_step()
                if not step:
                    # End of file
                    break
                if thermo_flag:
                    # Get thermo data from the step
                    thermo_flag = self.get_step_thermodata(step)
                
                # Write the step to the output file
                out.write_to_xyz(step)

                # Print the step number
                print('Step n. ', i, ' processed')
                # Increment the step counter
                i += 1

    def get_thermodata(self):
        """
        Retrieves the thermo data from the simulation data.
        If the thermo data is not found, prints a message and returns None.

        Returns
        -------
        thermo : DataFrame
            The thermo data as a pandas DataFrame.
        None :
            If no thermo data is found.
        """
        i = 0 # Counter for the number of steps processed
        thermo_flag = True # Flag for thermo data availability

        if self.thermo_data is None:
            # Get step data from the file
            step = self.file.get_next_step()

            while True: # Loop through the steps
                if not step:
                    # End of file
                    break

                elif thermo_flag:
                    # Check if thermo data is available in the step and get it
                    thermo_flag = self.get_step_thermodata(step)
                    # Get the next step
                    step = self.file.get_next_step()

                elif not thermo_flag:
                    # No thermo data found in the step
                    print('No thermo data found in the file')
                    break

                # Print the step number
                print('Step n. ', i, ' processed')
                # Increment the step counter
                i += 1

            if thermo_flag and self.thermo_keywords is not None:
                # Create a DataFrame from the thermo data
                thermo = pd.DataFrame(self.thermo_data,
                                      columns=self.thermo_keywords)
                return thermo
            else:
                # No thermo data found
                return None
        else:
            # Create a DataFrame from the thermo data
            thermo = pd.DataFrame(self.thermo_data,
                                  columns=self.thermo_keywords)
            return thermo

    def get_step_thermodata(self, step):
        """
        Retrieves the thermo data from the simulation step data.
        Append the thermo data to the thermo_data attribute.

        Parameters
        ----------
        step : dict
            The simulation step data.

        Returns
        -------
        thermo_flag : bool
            A boolean indicating if thermo data was found.

        Raises
        ------
        Exception
            If no thermo data is found in the step.
        """
        thermo_flag = True # Flag for thermo data availability

        if self.thermo_keywords is None:
            # Check if thermo data is available in the step
            thermo_flag = self.check_thermo_data(step)

            if thermo_flag:
                # Get thermo keywords from the step
                self.thermo_keywords = step['thermo']['keywords']
                self.thermo_data = []

        if thermo_flag:
            # Append thermo data to the thermo_data attribute
            self.thermo_data.append(step['thermo']['data'])
            return thermo_flag

        else:
            # No thermo data found in the step
            thermo_flag = False
            return thermo_flag

    def check_thermo_data(self, step):
        """
        Checks if thermo data is available in the simulation step data
        and if the thermo data has the same length.

        Parameters
        ----------
        step : dict
            The simulation step data.

        Returns
        -------
        bool
            True if thermo data is available and has the same length.
            False if thermo data is not available or has different lengths.
        """
        try:
            # Check if thermo data is available in the step
            thermo_keywords = step['thermo']['keywords']
            thermo_data = step['thermo']['data']
        except KeyError:
            # No thermo data found in the step
            return False
        else:
            # Check if thermo data has the same length
            if len(thermo_keywords) != len(thermo_data):
                return False
            return True

    def make_graphs(self, mode='display'):
        """
        Creates an instance of the GraphMaker class and generates graphs based
            on thermodynamic data.

        Parameters
        ----------
        mode : str
            The mode in which the graphs should be generated.
            Default is 'display'.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If an invalid mode is provided.
            Valid values are "display" and "interactive".
        """
        # Get thermo data
        thermo_df = self.get_thermodata()
        # Create GraphMaker object
        self.graphs = GraphMaker(thermo_df)

        # Generate graphs
        if not mode.startswith('d') and not mode.startswith('i'):
            # Invalid mode
            raise ValueError('Invalid mode. '
                             'Valid values are "display" and "interactive"')
        else:
            self.graphs.run(mode)
