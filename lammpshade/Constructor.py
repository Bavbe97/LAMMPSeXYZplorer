from lammpshade.YAMLReader import YAMLReader
from lammpshade.XYZWriter import XYZWriter
from lammpshade.GraphMaker import GraphMaker
import pandas as pd


"""
This module provides a Simulation class for processing LAMMPS simulation data.

Classes:
- Simulation

"""


class Simulation:
    """
    A class for processing LAMMPS simulation data.

    Attributes:
    file : YAMLReader
        The YAMLReader object for reading the simulation data file.
    thermo_keywords : list
        The list of thermo keywords.
    thermo_data : list
        The list of thermo data.
    graphs : GraphMaker
        The GraphMaker object for creating graphs.

    Methods:
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

        Parameters:
        - filepath: The path to the simulation data file.

        """
        self.file = YAMLReader(filepath)
        self.thermo_keywords = None
        self.thermo_data = None

    def convert_to_xyz(self, output, thermo_flag=True):
        """
        Converts the simulation data to XYZ format.

        Parameters:
        - output: The path to the output XYZ file.
        - thermo_flag: A boolean indicating if thermo data should be included.
            Default is True.
        
        Returns:
        - None

        """
        i = 0
        self.output = XYZWriter(output)
        with self.output as out:
            while True:
                step = self.file.get_next_step()
                if not step:
                    break
                if thermo_flag:
                    thermo_flag = self.get_step_thermodata(step)
                out.write_to_xyz(step)
                print('Step n. ', i, ' processed')
                i += 1

    def get_thermodata(self):
        """
        Retrieves the thermo data from the simulation data.

        Returns:
        - thermo: The thermo data as a pandas DataFrame.

        """
        i = 0
        thermo_flag = True
        if self.thermo_data is None:
            step = self.file.get_next_step()
            while True:
                if not step:
                    break

                elif thermo_flag:
                    thermo_flag = self.get_step_thermodata(step)
                    print('Step n. ', i, ' processed')
                    i += 1
                    step = self.file.get_next_step()

                elif not thermo_flag:
                    print('No thermo data found in the file')
                    break

            if thermo_flag:
                thermo = pd.DataFrame(self.thermo_data,
                                      columns=self.thermo_keywords)
                return thermo
            else:
                return None
        else:
            thermo = pd.DataFrame(self.thermo_data,
                                  columns=self.thermo_keywords)
            return thermo

    def get_step_thermodata(self, step):
        """
        Retrieves the thermo data from the simulation step data.
        Append the thermo data to the thermo_data attribute.

        Parameters:
        - step: The simulation step data.

        Returns:
        - thermo_flag: A boolean indicating if thermo data was found.

        Raises:
        - Exception: If no thermo data is found in the step.
        """
        thermo_flag = True
        if self.thermo_keywords is None:
            # Attempt to get thermo data from the step
            try:
                self.thermo_keywords = []
                self.thermo_keywords = step['thermo']['keywords']
            except KeyError('No thermo data found in the step'):
                # No thermo data found in the step
                print('No thermo data found in the file')
                thermo_flag = False
                # Return thermo_flag to indicate no thermo data found
                return thermo_flag
            else:
                # Append thermo data to the thermo_data attribute
                self.thermo_data = []
                self.thermo_data.append(step['thermo']['data'])
                return thermo_flag
        else:
            # Append thermo data to the thermo_data attribute
            self.thermo_data.append(step['thermo']['data'])
            return thermo_flag

    def make_graphs(self, mode='display'):
        """
        Creates an instance of the GraphMaker class and generates graphs based
            on thermodynamic data.

        Parameters:
            mode (str): The mode in which the graphs should be generated.
                Default is 'display'.

        Returns:
            None

        Raises:
            ValueError: If an invalid mode is provided.
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
