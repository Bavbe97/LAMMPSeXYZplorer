from lammpshade.YAMLReader import *
from lammpshade.XYZWriter import *
from lammpshade.GraphMaker import *
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
    - file: The YAMLReader object for reading the simulation data file.
    - thermo_keywords: The list of thermo keywords.
    - thermo_data: The list of thermo data.
    - graphs: The GraphMaker object for creating graphs.

    Methods:
    - __init__(self, filepath): Initializes the Simulation object.
    - convert_to_xyz(self, output): Converts the simulation data to XYZ format.
    - get_thermodata(self): Retrieves the thermo data from the simulation data.
    - make_graphs(self, interact=False): Creates graphs from the thermo data.

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
        self.graphs = None

    def convert_to_xyz(self, output):
        """
        Converts the simulation data to XYZ format.

        Parameters:
        - output: The path to the output XYZ file.

        """
        i = 0
        thermo_flag = True
        self.output = XYZWriter(output)
        with self.output as out:
            while True:
                step = self.file.get_next_step()
                if not step:
                    break
                if thermo_flag:
                    if self.thermo_keywords is None:
                        try:
                            self.thermo_keywords = step['thermo']['keywords']
                            self.thermo_data = []
                            self.thermo_data.append(step['thermo']['data'])
                        except:
                            print('No thermo data found in the file')
                            thermo_flag = False
                            pass
                    else:
                        self.thermo_data.append(step['thermo']['data'])
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
            self.thermo_data = []
            while True:
                step = self.file.get_next_step()
                if not step:
                    break
                if thermo_flag:
                    if self.thermo_keywords is None:
                        try:
                            self.thermo_keywords = step['thermo']['keywords']
                        except:
                            print('No thermo data found in the file')
                            thermo_flag = False
                            return None
                        self.thermo_keywords = step['thermo']['keywords']
    
                    self.thermo_data.append(step['thermo']['data'])
                print('Step n. ', i, ' processed')
                i += 1
            thermo = pd.DataFrame(self.thermo_data,
                                  columns=self.thermo_keywords)
            if (thermo == 0).all().all():
                print('No thermo data found in the file')
                return None
            else:
                return thermo

        else:
            thermo = pd.DataFrame(self.thermo_data,
                                  columns=self.thermo_keywords)
            return thermo

    def make_graphs(self, interact=False):
        """
        Creates graphs from the thermo data.

        Parameters:
        - interact: Whether to interactively display the graphs.

        """
        self.thermo_data = self.get_thermodata()
        self.graphs = GraphMaker(self.thermo_data, self.thermo_keywords,
                                 self.file)
        if not interact:
            self.graphs.make_graph()
        else:
            self.graphs.interact_graph()
        return
