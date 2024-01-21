# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:18:27 2024

@author: fbarb
"""
def read_yaml(file):
    i = 0
    step_reading = False

    for line in file:
        if line.startswith('---'):
            step_reading = True

        while step_reading:
            if ':' in line and '-' not in line:
                key = line.split(':')[0].strip()
                value = line.split(':')[1].strip()
                if value != '':
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
                            data_list.append(d_value)
                            step[key] = data_list
                            line = file.readline()
                        elif '-' in line and ':' in line:
                            d_key = line.replace(' ', '').replace('-', '').split(':')[0]
                            d_value = line.replace(' ', '').replace('-', '').split(':')[1].strip()
                            data_dic[d_key] = d_value
                            step[key] = data_dic
                            line = file.readline()
                        else:
                            data_reading = False

            elif line.startswith('...'):
                step_reading = False

            else:
                break

file_path = 'dump_file.yaml'
output = 'dump_file.xyz'
step = {}

if __name__ == "__main__":
    with open(file_path, 'r') as file:
        read_yaml(file)

