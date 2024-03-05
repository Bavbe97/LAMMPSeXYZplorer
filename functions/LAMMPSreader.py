# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 12:14:57 2024

@author: fbarb
"""

def convert_value(value):

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

def read_yaml(file, step):
    step_reading = False

    for line in file:
        if line.startswith('---'):
            step_reading = True

        while step_reading:
            if ':' in line and '-' not in line:
                key = line.split(':')[0].strip()
                value = line.split(':')[1].strip()
                if value != '':
                    value = convert_value(value)
                    step[key] = value
                    line = file.readline()

                else:
                    line = file.readline()
                    data_reading = True
                    data_list = []
                    data_dic = {}
                    while data_reading:
                        if '-' in line and ':' not in line:
                            d_value = line.split('- ')[1]
                            d_value = convert_value(d_value)
                            data_list.append(d_value)
                            step[key] = data_list
                            line = file.readline()
                        elif '-' in line and ':' in line:
                            d_key = line.replace(' ', '').replace('-', '').split(':')[0]
                            d_value = line.replace(' ', '').replace('-', '').split(':')[1].strip()
                            d_value = convert_value(d_value)
                            data_dic[d_key] = d_value
                            step[key] = data_dic
                            line = file.readline()
                        else:
                            data_reading = False

            elif line.startswith('...'):
                step_reading = False

            else:
                break