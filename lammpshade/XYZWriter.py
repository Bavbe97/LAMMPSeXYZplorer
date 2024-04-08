import pandas as pd
import os


class XYZWriter:
    """
    A class used to write data in XYZ format to a specified output file.

    ...

    Attributes
    ----------
    output : file object
        The output file where the data will be written.

    Methods
    -------
    write_to_xyz(step)
        Writes data in XYZ format to the output file.
    """
    has_written = False

    def __init__(self, filepath):
        # Check if the file ends with the right format (.xyz)
        if not filepath.lower().endswith('.xyz'):
            raise ValueError("File format must be .xyz")
        
        # If only the filename is given, create it in the "./xyz/" subdirectory
        if not os.path.exists(filepath):
            filepath = os.path.join(os.getcwd(), 'xyz', filepath)
        
        self.filepath = filepath
        self.output = None

    def __enter__(self):
        mode = 'a' if XYZWriter.has_written else 'w'
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        self.output = open(self.filepath, mode)
        XYZWriter.has_written = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.output:
            self.output.close()

    def write_to_xyz(self, step):
        """
        Writes the data to the specified output file.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file. It should contain the following keys:
            {
                'natoms': <number of atoms>,
                'box': <box data>
                'thermo': {
                    'keywords': <list of keywords>,
                    'data': <corresponding data for each keyword>
                },
                'keywords': <list of atom keywords>,
                'data': <list of lists containing atom data>
            }
        """

        # Check if the required data is present in the step dictionary
        self.data_check(step, ['natoms', 'data', 'keywords'], 'atoms data')
        # Check if the required data is present in the keywords list
        self.data_check(step['keywords'], ['element', 'x', 'y', 'z'], ' atoms coordinates')

        # Flag to check if thermo data is available
        thermo_check = [True]*2

        # Attempt to write number of atoms to .xyz output file
        self.output.write(str(step['natoms']) + '\n')

        # Attempt to process and write thermo data to .xyz output file
        try:
            # Remove 'c_' and 'v_' prefixes from keywords
            step['thermo']['keywords'] = [keyword.replace('c_', '').replace('v_', '') for keyword in step['thermo']['keywords']]

            # Create a string of key=value pairs
            thermo_data = '; '.join([f"{key}={val}" for key, val in
                                    zip(step['thermo']['keywords'],
                                        step['thermo']['data'])])

            # Check if box data is available
            if 'box' not in step and thermo_check[1] == True: 
                print('Box data was not found\n' +
                      'Program will continue without it')
                thermo_check[1] = False
            
            if 'box' in step:
                # Find the index of 'Time=' in the string
                index = thermo_data.index('Time=')
                index = index + thermo_data[index:].index(';') + 1

                # Insert box data into the string
                thermo_data = (thermo_data[:index] + ' Box=' + str(step['box'])[1:-1]
                        + ';' + thermo_data[index:])
            
            # Write the thermo data to the file
            self.output.write(thermo_data + '\n')

        except:
            if thermo_check[0] == True:
                print('Thermo_data was not found\n' + 
                      'Program will continue without it')
                thermo_check[0] = False
            self.output.write('\n')

        # Attempt to create a DataFrame from the atom data
        atoms_df = pd.DataFrame(step['data'], columns=step['keywords'])

        # List of keywords to be used for reordering the DataFrame columns
        keywords_lst = ['element', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy',
                        'fz', 'type']

        # Filter the DataFrame columns to include only the keywords in the list
        atoms_df = atoms_df.filter(keywords_lst, axis=1)

        # Write the atom data to the file
        atoms_df.to_csv(self.output, mode='a', index=False, header=False, sep=" ",
                        lineterminator='\n')

        
    def data_check(self, step, keys, data_type):
        """
        Checks if the required keys are present in the step dictionary.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.
        keys : list
            A list of keys that should be present in the step dictionary.

        Raises
        ------
        KeyError
            If the required keys are not found in the step dictionary.
        """
        for key in keys:
            if key not in step:
                raise KeyError(f"'{data_type}' not found in step.")
