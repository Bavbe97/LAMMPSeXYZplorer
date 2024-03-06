# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:25:10 2024

@author: fbarb
"""
import pandas as pd

class XYZWriter:
    def __init__(self, output):
        self.output = open(output, 'w')

    def write_to_xyz(self, step):
        """Writes data in XYZ format to the specified output file.

        Parameters
        ----------
        step : dict
            A dictionary containing information necessary for XYZ file generation.
            The dictionary 'step' should contain keys:
                 'natoms': The total number of atoms in the structure.
                 'data': A list of dictionaries where each dictionary represents
                      an atom's data.
                 'keywords': A list of strings representing the data keys for
                      each atom.
                - 'thermo': A dictionary containing information for thermodynamic
                      data.

        output : file object
            The output file object where the XYZ-formatted data will be written.

        Returns
        -------
        None
            The function writes the data to the specified output file."""

        # Print number of atoms to .xyz output file
        self.output.write(str(step['natoms']) + '\n')
        step['thermo']['keywords'] = [keyword.strip('c_').strip('v_') for
                                      keyword in step['thermo']['keywords']]
        thermo_data = '; '.join([f"{key}={val}" for key, val in
                                 zip(step['thermo']['keywords'],
                                     step['thermo']['data'])])
        index = thermo_data.index('Time=')
        index = index + thermo_data[index:].index(';') + 1
        thermo_data = (thermo_data[:index] + ' Box=' + str(step['box'])[1:-1]
                       + ';' + thermo_data[index:])
        self.output.write(thermo_data + '\n')

        atoms_df = pd.DataFrame(step['data'], columns=step['keywords'])

        keywords_lst = ['element', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy',
                        'fz', 'type']

        atoms_df = atoms_df.filter(keywords_lst, axis=1)
        if 'element' and 'x' and 'y' and 'z' not in atoms_df.columns:
            print('Error')
        else:
            atoms_df.to_csv(self.output, mode='a', index=False, header=False, sep=" ",
                            lineterminator='\n')
            
    def close_file(self):
        self.output.close()
        return
