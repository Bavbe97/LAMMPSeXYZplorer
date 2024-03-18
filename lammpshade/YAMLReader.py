# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:28:31 2024

@author: fbarb
"""


class YAMLReader:
    def __init__(self, filename = None):
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
       value: str If the content doesn't match any of the conversion criteria,
           the original string is returned unchanged.

        """
        value = value.strip()

        if value.isdigit(): #Convert to int
            return int(value)

        if '.' in value: #Convert to float
            try:
                return float(value)
            except ValueError:
                pass

        if value.startswith('[') and value.endswith(']'): #Convert to list
            elements = value[1:-1].split(',')
            elements = [elem.strip() for elem in elements]
            converted_elements = []
            for elem in elements:
                if elem.isdigit(): #Convert list element to int
                    converted_elements.append(int(elem))
                elif '.' in elem: #Convert list element to float
                    try:
                        converted_elements.append(float(elem))
                    except ValueError:
                        converted_elements.append(elem)
                elif not elem:
                    continue
                else:
                    converted_elements.append(elem)

            return converted_elements #Return list

        return value #Return int, float or string
        pass

    def get_next_step(self):
        step = {}
        line = self.file.readline()
        while True:
            if not line:
                # End of file reached
                break

            if line.startswith('---'):
                # Start of a new step
                line = self.file.readline()
                continue

            if line.startswith('...'):
                # End of the current step
                self.current_step = step
                return step

            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if value:
                    value = self.convert_value(value)
                    step[key] = value
                    line = self.file.readline()
                else:
                    line = self.file.readline()
                    data_reading = True
                    data_list = []
                    data_dic = {}
                    while data_reading:
                        if not line or line.startswith('...'):
                            step_reading = False
                            self.current_step = step
                            return step
                        elif '-' in line and ':' not in line:
                            d_value = line.split('- ')[1]
                            d_value = self.convert_value(d_value)
                            data_list.append(d_value)
                            step[key] = data_list
                            line = self.file.readline()
                        elif '-' in line and ':' in line:
                            d_key = line.replace(' ', '').replace('-', '').split(':')[0]
                            d_value = line.replace(' ', '').replace('-', '').split(':')[1].strip()
                            d_value = self.convert_value(d_value)
                            data_dic[d_key] = d_value
                            step[key] = data_dic
                            line = self.file.readline()
                        else:
                            data_reading = False
                            continue
            else:
                line = self.file.readline()
        # Close the file when done reading
        self.file.close()
        return step

    def get_units(self, keyword):
        # Check if 'units' attribute is not found in self.current_step
        keyword = keyword.lower()
        if 'units' not in self.current_step:
            raise ValueError("Units attribute not found in current step" +
                             "\n Check  LAMMPS output file")
    
        # Obtain the value of 'units' attribute
        units = self.current_step['units']
    
        # Map units to their corresponding unit format
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

        # Check if the 'units' value exists in the mappings
        if units in units_mappings:
            # Check if the keyword matches exactly in the mappings for the corresponding 'units'
            if keyword in units_mappings[units]:
                return units_mappings[units][keyword]

            # Check if any prefix matches using startswith()
            for prefix, unit in units_mappings[units].items():
                if keyword.startswith(prefix):
                    return unit

            # If no matching prefix found, raise an error
            raise ValueError("Units information not available for the given keyword")
        else:
            raise ValueError("Invalid units: {}".format(units) +
                             '\n Check LAMMPS output file and documentation.')
