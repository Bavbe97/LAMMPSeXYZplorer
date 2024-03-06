# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:28:31 2024

@author: fbarb
"""


class YAMLReader:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'r')
        self.current_step = None

    def convert_value(self, value):
        """

        Converts a string variable to an INT, FLOAT, or LIST based on its content.

       Parameters
       ----------
       value : str
           String that needs to be converted.

       Returns ------- int(value) : int If the content of the string contains only digits, it's converted to an integer.
       float(value): float If the string contains a dot ('.') and the content is in a valid floating-point format,
       it's converted to a float. converted_elements: list If the string starts and ends with square brackets ('[', ']'),
       it's converted to a list of elements. Elements in the list are converted to integers, floats, or remain as strings
       based on their content. value: str If the content doesn't match any of the conversion criteria, the original
       string is returned unchanged.

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
        step_reading = False
        line = self.file.readline()
        while line:
            if line.startswith('---'):
                step_reading = True
                line = self.file.readline()
                continue

            while step_reading:
                if ':' in line and '-' not in line:
                    key = line.split(':')[0].strip()
                    value = line.split(':')[1].strip()
                    if value != '':
                        value = self.convert_value(value)
                        step[key] = value
                        line = self.file.readline()
                        continue
                    else:
                        line = self.file.readline()
                        data_reading = True
                        data_list = []
                        data_dic = {}
                        while data_reading:
                            if '-' in line and ':' not in line:
                                d_value = line.split('- ')[1]
                                d_value = self.convert_value(d_value)
                                data_list.append(d_value)
                                step[key] = data_list
                                line = self.file.readline()
                            elif '-' in line and ':' in line:
                                d_key = line.replace(' ', '').replace('-', '').split(':')[0]
                                d_value = line.replace(' ', '').replace('-', '').split(':')[1].strip()
                                d_value = self.convert_value(d_value)  # missing possibility of list
                                data_dic[d_key] = d_value
                                step[key] = data_dic
                                line = self.file.readline()
                            else:
                                data_reading = False
                                continue
                elif line.startswith('...'):
                    step_reading = False
                    self.current_step = step
                    return step
                    break
                else:
                    step_reading = False
                    continue
        # If we reach here, it means there are no more steps
        self.file.close()
        return

if __name__ == '__main__':
    yaml_reader = YAMLReader('./examples/input_example.yaml')
    
    while True:
        step = yaml_reader.get_next_step()
        print(step)
        if not step:
            break