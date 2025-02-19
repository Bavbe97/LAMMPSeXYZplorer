import pandas as pd
import os


"""
This module contains the XYZWriter class for writing data in XYZ format to a
specified output file.
"""


class XYZWriter:
    """
    A class used to write data in XYZ format to a specified output file.
    Can be used as a context manager to open and close the output file.

    ...

    Attributes
    ----------
    output : file object
        The output file where the data will be written.

    Methods
    -------
    __init__(filepath)
        Initializes the XYZWriter object with the specified output file path.
    __enter__()
        Opens the output file for writing when the object is used as a context
        manager.
    __exit__()
        Closes the output file when the object is used as a context manager.
    write_to_xyz(step)
        Writes data in XYZ format to the output file.
    check_step_data(step)
        Checks if the required data is present in the step dictionary.
    process_and_write_natoms(step)
        Writes the number of atoms to the output file.
    process_and_write_thermo_data(step)
        Processes and writes thermo data to the output file.
    process_thermo_data(step)
        Processes thermo data to be written to the output file.
    write_thermo_data(thermo_data)
        Writes thermo data to the output file.
    process_box_data(step, thermo_data)
        Processes box data to be written to the output file.
    create_and_write_atom_data(step)
        Creates a DataFrame from the atom data and writes it to the output
        file.
    process_atom_data_df(atoms_df)
        Processes the atom data DataFrame to match the required format.
    data_check(step, keys, data_type)
        Checks if the required keys are present in the step dictionary.
    """

    def __init__(self, filepath):
        """
        Initializes the XYZWriter object with the specified output file path.

        Parameters
        ----------
        filepath : str
            The path to the output file where the data will be written.
            If only the filename is given, the file will be created in the
            "./xyz/" subdirectory.

        Raises
        ------
        ValueError
            If the file format is not .xyz.
        """
        # Check if the file ends with the right format (.xyz)
        if not filepath.lower().endswith('.xyz'):
            raise ValueError("File format must be .xyz")

        # If only the filename is given, create it in the "./xyz/" subdirectory
        if not os.path.exists(filepath):
            filepath = os.path.join(os.getcwd(), 'xyz', filepath)

        self.filepath = filepath  # Path to the output file
        self.output = None  # File object to write data to
        self.has_written = False  # Flag to check if the file has been written
        self.thermo_check = [True]*2  # Flag to check for thermo and box data

    def __enter__(self):
        """
        Opens the output file for writing when the object is used as a context
        manager.
        If the output file does not exists, it will be created.
        If the output file is already written, it will be opened in append
        mode.
        """
        mode = 'a' if self.has_written else 'w'
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        self.output = open(self.filepath, mode)
        self.has_written = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the output file when the object is used as a context manager.
        """
        if self.output:
            self.output.close()

    def write_to_xyz(self, step):
        """
        Writes the data to the specified output file.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file. It
            should AT LEAST contain the following keys:
            {
                'natoms': <number of atoms>,
                'keywords': <list of atom keywords>,
                'data': <list of lists containing atom data>
            }

        Returns
        -------
        None
        """

        # Check if the required data is present in the step dictionary
        self.check_step_data(step)

        # Write number of atoms to .xyz output file
        self.process_and_write_natoms(step)

        # Attempt to process and write thermo data to .xyz output file
        if self.thermo_check[0] is True:
            self.thermo_check = self.process_and_write_thermo_data(step)

        # Create and write atom data to .xyz output file
        self.create_and_write_atom_data(step)

    def check_step_data(self, step):
        """
        Checks if the required data to write an XYZ file is present in the
        step dictionary.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the required data is not found in the step dictionary.
        """
        # Check if the required data is present in the step dictionary
        self.data_check(step, ['natoms', 'data', 'keywords'], 'atoms data')
        # Check if the required data is present in the keywords list
        self.data_check(step['keywords'], ['element', 'x', 'y', 'z'],
                        ' atoms coordinates')

    def process_and_write_natoms(self, step):
        """
        Writes the number of atoms to the specified output file.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the number of atoms is not found in the step dictionary.
        TypeError
            If the number of atoms is not a positive integer.
        """
        # Attempt to write number of atoms to .xyz output file
        if 'natoms' not in step:
            raise KeyError("Number of atoms is not found in the step" +
                           "dictionary\n" +
                           "Program will be terminated")

        if not isinstance(step['natoms'], int) or step['natoms'] < 0:
            raise TypeError("Number of atoms must be a positive integer\n" +
                            "Program will be terminated")

        else:
            self.output.write(str(step['natoms']) + '\n')

    def process_and_write_thermo_data(self, step):
        """
        If thermo data is available, processes and writes it to the output
        file.
        If thermo data is not found, a newline character is written to the
        file.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.
        thermo_check : list
            A list containing two boolean values to check if thermo and box
            data are available.

        Returns
        -------
        thermo_check : list
            A list containing two boolean values to check if thermo and box
            data are available.
        """

        if self.thermo_check[0] is True:
            # Process thermo data
            self.thermo_check, thermo_data = self.process_thermo_data(step)

        if self.thermo_check[1] is True:
            # Process box data
            self.thermo_check, thermo_data = self.process_box_data(step,
                                                                   thermo_data)

        # Write thermo data
        self.write_thermo_data(thermo_data)

        return self.thermo_check

    def process_thermo_data(self, step):
        """
        Processes thermo data to be written to the output file.
        If thermo data is not found, a message is printed to the console.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.
        thermo_check : list
            A list containing two boolean values to check if thermo and box
            data are available.

        Returns
        -------
        thermo_check : list
            A list containing two boolean values to check if thermo and box
            data are available.
        thermo_data : str
            A string containing the thermo data to be written to the output
            file.
        """

        # Attempt to process and write thermo data to .xyz output file
        try:
            # Remove 'c_' and 'v_' prefixes from keywords
            step['thermo']['keywords'] = [
                keyword.replace('c_', '').replace('v_', '')
                for keyword in step['thermo']['keywords']
            ]

            # Create a string of key=value pairs
            thermo_data = '; '.join([
                f"{key}={val}"
                for key, val in zip(step['thermo']['keywords'],
                                    step['thermo']['data'])
            ])

        # If thermo data is not found, continue without it
        except Exception:
            if self.thermo_check[0] is True:
                print('Thermo_data was not found\n' +
                      'Program will continue without it')
                thermo_data = ''
                self.thermo_check[0] = False

        return self.thermo_check, thermo_data

    def write_thermo_data(self, thermo_data):
        """
        Checks if thermo data is available and writes it to the output file.
        If thermo data is not found, a newline character is written to the
        file.

        Parameters
        ----------
        thermo_data : str
            A string containing the thermo data to be written to the output
            file.
        thermo_check : list
            A list containing two boolean values to check if thermo and box
            data are available.

        Returns
        -------
        None
        """

        if self.thermo_check[0] is True:
            # Write the thermo data to the file
            self.output.write(thermo_data + '\n')
        else:
            # Write a newline character if thermo data is not found
            self.output.write('\n')

    def process_box_data(self, step, thermo_data):
        """
        Processes box data to be written to the output file.
        If box data is not found, a message is printed to the console.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.
        thermo_check : list
            A list containing two boolean values to check if thermo and box
            data are available.
        thermo_data : str
            A string containing the thermo data to be written to the output
            file.

        Returns
        -------
        thermo_check : list
            A list containing two boolean values to check if thermo and box
            data are available.
        thermo_data : str
            A string containing the updated thermo data cointaining the box
            data to be written to the output file.
        """
        # Check if box data is available
        if 'box' not in step and self.thermo_check[1] is True:
            print('Box data was not found\n' +
                  'Program will continue without it')
            self.thermo_check[1] = False

        if 'box' in step and self.thermo_check[0] is True:
            try:
                # Find the index of 'Time=' in the string
                index = thermo_data.index('Time=')
                index = index + thermo_data[index:].index(';') + 1

                # Insert box data into the string
                thermo_data = (thermo_data[:index] + ' Box=' +
                               str(step['box'])[1:-1] + ';' +
                               thermo_data[index:])

            except Exception:
                # If 'Time' is not found in the string
                print('Time was not found in thermo_data\n' +
                      'Program will continue without thermo_data')
                self.thermo_check[0] = False
                self.thermo_check[1] = False

        return self.thermo_check, thermo_data

    def create_and_write_atom_data(self, step):
        """
        Creates a DataFrame from the atom data, filters it, and writes it to
        the output file with a specific format.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.

        Returns
        -------
        None
        """
        # Create a DataFrame from the atom data
        atoms_df = pd.DataFrame(step['data'], columns=step['keywords'])

        # Reorder the DataFrame columns
        atoms_df = self.process_atom_data_df(atoms_df)

        # Write the atom data to the file
        atoms_df.to_csv(self.output, mode='a', index=False, header=False,
                        sep=" ", lineterminator='\n')

    def process_atom_data_df(self, atoms_df):
        """
        Filters the DataFrame columns to include only the keywords needed for
        writing the atom data to the output file.
        The keywords are reordered to match the required format.

        Parameters
        ----------
        atoms_df : DataFrame
            A DataFrame containing the atom data.

        Returns
        -------
        atoms_df : DataFrame
            A DataFrame containing the filtered atom data.
        """
        # List of keywords to be used for reordering the DataFrame columns
        keywords_lst = ['element', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy',
                        'fz', 'type']

        # Filter the DataFrame columns to include only the keywords in the list
        atoms_df = atoms_df.filter(keywords_lst, axis=1)

        return atoms_df

    def data_check(self, step, keys, data_type):
        """
        Checks if the required keys are present in the step dictionary.

        Parameters
        ----------
        step : dict
            A dictionary containing the data to be written to the file.
        keys : list
            A list of keys that should be present in the step dictionary.

        Returns
        -------
        bool
            True if the required keys are present in the step dictionary.

        Raises
        ------
        KeyError
            If the required keys are not found in the step dictionary.
        """
        data_check = True
        for key in keys:
            if key not in step:
                data_check = False
                raise KeyError(f"'{data_type}' not found in step.")

        if data_check:
            return True
