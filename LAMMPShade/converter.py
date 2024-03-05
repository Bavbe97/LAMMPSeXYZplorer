
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 12:14:57 2024

@author: fbarb
"""

import pandas as pd

#Reader functions

def convert_value(value):
    """Converts a string variable to an INT, FLOAT, or LIST based on its content.

   Parameters
   ----------
   value : str
       String that needs to be converted.

   Returns 
   ------- 
   int(value) : int 
       If the content of the string contains only digits, it's converted to 
       an integer.
   float(value): float 
       If the string contains a dot ('.') and the content is in a valid 
       floating-point format, it's converted to a float. 
   converted_elements: list
       If the string starts and ends with square brackets ('[', ']'), it's 
       converted to a list of elements. 
           Elements in the list are converted to integers, floats, or remain as 
           strings based on their content. 
   value: str 
       If the content doesn't match any of the conversion criteria, 
       the original string is returned unchanged."""
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


def write_xyz(step, output):
    """Writes data in XYZ format to the specified output file.

    Parameters
    ----------
    step : dict
        A dictionary containing information necessary for XYZ file generation.
        The dictionary 'step' should contain keys:
            - 'natoms': The total number of atoms in the structure.
            - 'data': A list of dictionaries where each dictionary represents 
                an atom's data.
            - 'keywords': A list of strings representing the data keys for 
                each atom.
            - 'thermo': A dictionary containing information for thermodynamic 
            data.

    output : file object
        The output file object where the XYZ-formatted data will be written.

    Returns
    -------
    None
        The function writes the data to the specified output file."""
  
    with open(output, 'a') as out:
        #Print number of atoms to .xyz output file 
        out.write(str(step['natoms']) + '\n') 
        step['thermo']['keywords'] = [keyword.strip('c_').strip('v_') for 
                                      keyword in step['thermo']['keywords']]
        thermo_data = '; '.join([f"{key}={val}" for key, val in 
                                 zip(step['thermo']['keywords'], 
                                     step['thermo']['data'])])
        index = thermo_data.index('Time=')
        index = index + thermo_data[index:].index(';') + 1
        thermo_data = thermo_data[:index] + ' Box=' + str(step['box'])[1:-1] 
        + ';' + thermo_data[index:]
        out.write(thermo_data + '\n')
    
        atoms_df = pd.DataFrame(step['data'], columns=step['keywords'])
        
        keywords_lst = ['element', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy',
                        'fz', 'type']
        
        atoms_df = atoms_df.filter(keywords_lst, axis=1)
        if 'element' and 'x' and 'y' and 'z' not in atoms_df.columns:
            print('Error')
            return
        else:
            atoms_df.to_csv(out,mode='a',index=False, header=False, sep=" ",
                            lineterminator='\n')
            return
        

def read_yaml(file, step):
    """Reads lines from a file and processes YAML-like formatted data, generated as an OUTPUT of a LAMMPS calculation.

    Parameters
    ----------
    file : file object
        The file object containing YAML-like formatted data to be processed.

    step: dictionary
        Dictionary in which the function stores each step of the simulation 
            (Data is overwritten at each step)

    Notes
    -----
    - The function iterates through each line in the provided file.
    - Lines starting with '---' indicate the beginning of step readings.
    - During step readings:
        - Lines with ':' (colon) and without '-' (hyphen) are treated as 
          key-value pairs.
        - Empty values trigger subsequent data readings, forming a list or a 
          dictionary of values.
        - If a value is non-empty, it's converted and assigned to the 
          corresponding key in the 'step' dictionary.
        - Lines starting with '...' mark the end of step readings and prompt 
          writing data to an output file if provided.
    - Utilizes a helper function 'convert_value' to handle value conversions
      based on content.

    Returns
    -------
    None"""
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
                            d_key = (line.replace(' ', '').replace('-', '')
                                     .split(':')[0])
                            d_value = (line.replace(' ', '').replace('-', '')
                                       .split(':')[1].strip())
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
            