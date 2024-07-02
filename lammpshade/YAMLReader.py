"""
This module provides a class for reading YAML-formatted files and extracting
data.
"""


class YAMLReader:
    """
    A class to read YAML-formatted files and extract data.

    ...

    Attributes
    ----------
    filename : str
        The path to the YAML file.
    file : file
        The file object representing the opened YAML file.
    current_step : dict
        A dictionary containing data from the current step.

    Methods
    -------
    __init__(filename)
        Initializes a YAMLReader object.
    convert_value(value)
        Converts a string variable to an INT, FLOAT, or LIST based on its
        content.
    get_next_step()
        Reads the next step from the YAML file and returns its data.

    """

    def __init__(self, filename):
        """
        Initializes a YAMLReader object.

        Parameters
        ---------
        filename : str
            The path to the YAML file. Defaults to None.

        Raises
        ------
        FileNotFoundError
            If the specified file is not found.
        """
        self.filename = filename  # Path to the YAML file
        self.current_step = None  # Data from the current step
        try:
            # Open the file
            self.file = open(filename, 'r')

        # Handle FileNotFoundError
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found.")

    def convert_value(self, value):
        """
        Converts a string variable to an INT, FLOAT, or LIST based on its
        content.

        Parameters
        ----------
        value : str
            String that needs to be converted.

        Returns
        -------
        int(value) : int
            If the content of the string contains only digits, it's converted
            to an integer.
        float(value) : float
            If the string contains a dot ('.') and the content is in a valid
            floating-point format, it's converted to a float.
        converted_elements : list
            If the string starts and ends with square brackets ('[', ']'),
            it's converted to a list of elements. Elements in the list are
            converted to integers, floats, or remain as strings based on their
            content.
        value : str
            If the content doesn't match any of the conversion criteria, the
            original string is returned unchanged.
        """
        # Assure right formatting of the value
        value = value.strip()

        int_value = self.convert_to_int(value)
        if int_value is not None:
            return int_value

        float_value = self.convert_to_float(value)
        if float_value is not None:
            return float_value

        list_value = self.convert_to_list(value)
        if list_value is not None:
            return list_value

        return value

    def convert_to_int(self, value):
        """
        Converts a string variable to an INT based on its content.

        Parameters
        ----------
        value : str
            String that needs to be converted.

        Returns
        -------
        int(value) : int
            If the content of the string contains only digits, it's converted
            to an integer.
        None : None"""
        if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
            return int(value)
        return None

    def convert_to_float(self, value):
        """
        Converts a string variable to a FLOAT based on its content.

        Parameters
        ----------
        value : str
            String that needs to be converted.

        Returns
        -------
        float(value) : float
            If the string contains a dot ('.') and the content is in a valid
            floating-point format, it's converted to a float.
        None : None
        """
        if '.' in value:
            # Try to convert it into float
            try:
                return float(value)
            except ValueError:
                pass
        return None

    def convert_to_list(self, value):
        """
        Converts a string variable to a LIST based on its content.

        Parameters
        ----------
        value : str
            String that needs to be converted.

        Returns
        -------
        converted_elements : list
            If the string starts and ends with square brackets ('[', ']'),
            it's converted to a list of elements. Elements in the list are
            converted to integers, floats, or remain as strings based on their
            content.
        None : None
        """
        # Check if the value is a list
        if value.startswith('[') and value.endswith(']'):
            elements = value[1:-1].split(',')
            elements = [elem.strip() for elem in elements]
            converted_elements = []
            for elem in elements:
                # Try to convert to int
                int_value = self.convert_to_int(elem)
                if int_value is not None:
                    converted_elements.append(int_value)
                else:
                    # Try to convert to float
                    float_value = self.convert_to_float(elem)
                    if float_value is not None:
                        converted_elements.append(float_value)
                    else:
                        # If the element is not a number, keep it as a string
                        converted_elem = elem
                        # Check if the element is empty
                        if converted_elem != '':
                            converted_elements.append(converted_elem)
            # Return the list
            return converted_elements
        # Return None if the value is not a list
        return None

    def get_next_step(self):
        """
        Reads the next step from the YAML file and returns its data.
        The data is stored in a dictionary.

        Returns
        -------
        step :  dict
            A dictionary containing data from the next step.
        """
        step = {}
        line = self.file.readline()
        while True:
            if not line:
                # If the end of file is reached, break the loop
                break

            if line.startswith('---'):
                # Start of a new step
                line = self.file.readline()
                continue

            if line.startswith('...'):
                # End of the current step, exit
                self.current_step = step
                return step

            if ':' in line:
                # Check for a key-value pair
                key, value = self.process_key_value_pair(line)
                if value:
                    step[key] = value
                    line = self.file.readline()
                else:
                    # Check for a key - list or key - dictionary pair
                    line = self.file.readline()
                    data_reading = True
                    data_list = []
                    data_dic = {}
                    while data_reading:
                        if not line or line.startswith('...'):
                            # Return function if the step ends abruptly
                            self.current_step = step
                            return step
                        elif '-' in line:
                            if ':' not in line:
                                # Get list
                                data_list, line = self.process_list(line)
                                step[key] = data_list
                            else:
                                # Get dictionary
                                data_dic, line = self.process_dictionary(line)
                                step[key] = data_dic
                        else:
                            # Exit loop
                            data_reading = False
                            continue
            else:
                # Ensure reading proceeds
                line = self.file.readline()
        # Close the file when done reading
        self.file.close()
        return step

    def process_key_value_pair(self, line):
        """
        Processes a line containing a key-value pair.

        Parameters
        ----------
        line : str
            A string containing a key-value pair.

        Returns
        -------
        key : str
            The key extracted from the line.
        value : str
            The value extracted from the line.
        """
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        if value:
            value = self.convert_value(value)
        return key, value

    def process_list(self, initial_line):
        """
        Processes a line containing a list.

        Parameters
        ----------
        initial_line : str
            A string containing the first element of the list.

        Returns
        -------
        data_list : list
            A list containing the elements of the list.
        line : str
            The next line after the list.
        """
        data_list = []
        line = initial_line
        while '- ' in line and ':' not in line:
            d_value = line.split('- ')[1].strip()
            d_value = self.convert_value(d_value)
            data_list.append(d_value)
            line = self.file.readline()
        return data_list, line

    def process_dictionary(self, initial_line):
        """
        Processes a line containing a dictionary.

        Parameters
        ----------
        initial_line : str
            A string containing the first element of the dictionary.

        Returns
        -------
        data_dic : dict
            A dictionary containing the elements of the dictionary.
        line : str
            The next line after the dictionary.
        """
        data_dic = {}
        line = initial_line
        while '- ' in line and ':' in line:
            d_key, d_value = line.replace(' ', '').split(':', 1)
            d_key = d_key.replace('-', '').strip()
            d_value = self.convert_value(d_value.strip())
            data_dic[d_key] = d_value
            line = self.file.readline()
        return data_dic, line
