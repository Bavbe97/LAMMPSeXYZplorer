"""
This module provides a class for reading YAML-formatted files and extracting data.

Module Attributes:
- None

Classes:
- YAMLReader: A class to read YAML-formatted files and extract data.
"""

class YAMLReader:
    """
    A class to read YAML-formatted files and extract data.

    Attributes:
    - filename (str): The path to the YAML file.
    - file (file object): The file object representing the opened YAML file.
    - current_step (dict): A dictionary containing data from the current step.
    """

    def __init__(self, filename):
        """
        Initializes a YAMLReader object.

        Parameters:
        - filename (str, optional): The path to the YAML file. Defaults to None.

        Raises:
        - FileNotFoundError: If the specified file is not found.
        """
        self.filename = filename
        self.current_step = None
        try:
            self.file = open(filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found.")

    def convert_value(self, value):
        """
        Converts a string variable to an INT, FLOAT, or LIST based on its content.

        Parameters:
        - value (str): String that needs to be converted.

        Returns:
        - int(value) (int): If the content of the string contains only digits, it's converted to an integer.
        - float(value) (float): If the string contains a dot ('.') and the content is in a valid floating-point format, it's converted to a float.
        - converted_elements (list): If the string starts and ends with square brackets ('[', ']'), it's converted to a list of elements. Elements in the list are converted to integers, floats, or remain as strings based on their content.
        - value (str): If the content doesn't match any of the conversion criteria, the original string is returned unchanged.
        """
        # Assure right formatting of the value
        value = value.strip()

        # Try to convert
        if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
            return int(value)

        if '.' in value:
            # Try to convert it into float
            try:
                return float(value)
            except ValueError:
                pass

        # Check if the value is a list
        if value.startswith('[') and value.endswith(']'):
            # Get elements
            elements = value[1:-1].split(',')
            elements = [elem.strip() for elem in elements]
            converted_elements = []
            # Try to convert the elements
            for elem in elements:
                if elem.isdigit() or (elem.startswith('-') and elem[1:].isdigit()):
                    converted_elements.append(int(elem))
                elif '.' in elem:
                    try:
                        converted_elements.append(float(elem))
                    except ValueError:
                        converted_elements.append(elem)
                elif not elem:
                    continue
                else:
                    converted_elements.append(elem)

            return converted_elements

        return value

    def get_next_step(self):
        """
        Reads the next step from the YAML file and returns its data.

        Returns:
        - dict: A dictionary containing data from the next step.
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
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if value:
                    value = self.convert_value(value)
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
                            step_reading = False
                            self.current_step = step
                            return step
                        elif '-' in line and ':' not in line:
                            # Get list
                            d_value = line.split('- ')[1]
                            d_value = self.convert_value(d_value)
                            data_list.append(d_value)
                            step[key] = data_list
                            line = self.file.readline()
                        elif '-' in line and ':' in line:
                            # Get dictionary
                            d_key = line.replace(' ', '').split(':')[0].replace('-', '')
                            d_value = line.split(':')[1]
                            d_value = self.convert_value(d_value)
                            data_dic[d_key] = d_value
                            step[key] = data_dic
                            line = self.file.readline()
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
