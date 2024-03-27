# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:28:31 2024

@author: fbarb
"""

import re

units_mappings = {
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

class YAMLReader:
    """
    A class to read YAML-formatted files and extract data.

    Attributes:
    - filename (str): The path to the YAML file.
    - file (file object): The file object representing the opened YAML file.
    - current_step (dict): A dictionary containing data from the current step.
    """
    def __init__(self, filename = None):
        """
        Initializes a YAMLReader object.

        Parameters:
        - filename (str, optional): The path to the YAML file. Defaults to None.
        """
        self.filename = filename
        if self.filename:
            self.file = open(filename, 'r')
        self.current_step = None

    def convert_value(self, value):
        """

        Converts a string variable to an INT, FLOAT, or LIST based on its content.

       Parameters
       ----------
       value : str
           String that needs to be converted.

       Returns
       -------
       int(value) : int
           If the content of the string contains only digits, it's converted
           to an integer.
       float(value): float
           If the string contains a dot ('.') and the content is in a valid
           floating-point format, it's converted to a float.
        converted_elements: list
            If the string starts and ends with square brackets ('[', ']'),
            it's converted to a list of elements. Elements in the list are
            converted to integers, floats, or remain as strings based on
            their content.
       value: str 
           If the content doesn't match any of the conversion criteria,
           the original string is returned unchanged.

        """
        # Assure right formatting of the value
        value = value.strip()

        # Try to convert

        if value.isdigit():
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
                if elem.isdigit():
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
                            d_key = line.replace(' ', '').replace('-', '').split(':')[0]
                            d_value = line.replace(' ', '').replace('-', '').split(':')[1].strip()
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

