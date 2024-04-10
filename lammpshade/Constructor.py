from lammpshade.YAMLReader import *
from lammpshade.XYZWriter import *
from lammpshade.GraphMaker import *
import pandas as pd


class Simulation:
    def __init__(self, filepath):
        self.file = YAMLReader(filepath)
        self.thermo_keywords = None
        self.thermo_data = None
        self.graphs = None

    def convert_to_xyz(self, output):
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
        self.thermo_data = self.get_thermodata()
        self.graphs = GraphMaker(self.thermo_data, self.thermo_keywords,
                                 self.file)
        if not interact:
            self.graphs.make_graph()
        else:
            self.graphs.interact_graph()
        return
