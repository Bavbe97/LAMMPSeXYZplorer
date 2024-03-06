# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:10:30 2024

@author: fbarb
"""

#missin ...
#inverted --- ...

#missing data type for xyz
#bad formatting
#unable to open file
#unable to find file

import io
import unittest

from lammpshade import convert_value

class TestConvertValue(unittest.TestCase):

    def test_convert_integer(self):
        self.assertEqual(convert_value('123'), 123)

    def test_convert_float(self):
        self.assertEqual(convert_value('3.14'), 3.14)

    def test_convert_list(self):
        self.assertEqual(convert_value('[1, 2, 3]'), [1, 2, 3])

    def test_convert_mixed_list(self):
        self.assertEqual(convert_value('[1, 2.5, apple, 4]'), [1, 2.5, 'apple', 4])

    def test_convert_string(self):
        self.assertEqual(convert_value('hello'), 'hello')

    def test_convert_empty_string(self):
        self.assertEqual(convert_value(''), '')

    def test_convert_whitespace_string(self):
        self.assertEqual(convert_value('  '), '')

    def test_convert_invalid_float(self):
        self.assertEqual(convert_value('3.14.15'), '3.14.15')

    def test_convert_invalid_list(self):
        self.assertEqual(convert_value('[1, 2, ]'), [1, 2, 0])

    def test_convert_invalid_list_element(self):
        self.assertEqual(convert_value('[1, 2, three]'), [1, 2, 'three'])

    def test_convert_invalid_value(self):
        self.assertEqual(convert_value('apple'), 'apple')

    def test_convert_value_with_whitespace(self):
        self.assertEqual(convert_value('  123  '), 123)

from lammpshade import write_xyz


class TestWriteXYZ(unittest.TestCase):

    def test_write_xyz_basic(self):
        step = {
            'natoms': 3,
            'data': [
                {'element': 'C', 'x': 0.0, 'y': 0.0, 'z': 0.0},
                {'element': 'H', 'x': 1.0, 'y': 1.0, 'z': 1.0},
                {'element': 'O', 'x': 2.0, 'y': 2.0, 'z': 2.0}
            ],
            'keywords': ['element', 'x', 'y', 'z'],
            'thermo': {
                'keywords': ['c_Temperature', 'v_Temperature'],
                'data': [300, 400],
                'box': [10, 10, 10]
            }
        }
        output = io.StringIO()
        write_xyz(step, output)
        expected_output = "3\nTemperature=300 Box=10, 10, 10; Temperature=400\nC 0.0 0.0 0.0\nH 1.0 1.0 1.0\nO 2.0 2.0 2.0\n"
        self.assertEqual(output.getvalue(), expected_output)

    def test_write_xyz_error(self):
        step = {
            'natoms': 2,
            'data': [
                {'element': 'C', 'x': 0.0, 'y': 0.0, 'z': 0.0},
                {'element': 'H', 'vx': 1.0, 'vy': 1.0, 'vz': 1.0}
            ],
            'keywords': ['element', 'x', 'y', 'z'],
            'thermo': {
                'keywords': ['c_Temperature', 'v_Temperature'],
                'data': [300, 400],
                'box': [10, 10, 10]
            }
        }
        output = io.StringIO()
        write_xyz(step, output)
        expected_output = "Error\n"
        self.assertEqual(output.getvalue(), expected_output)

from lammpshade import read_yaml

class TestReadYAML(unittest.TestCase):

    def test_read_yaml_basic(self):
        yaml_data = """---
        Temperature: 300
        Pressure: 1.0
        Energy: -1000.0
        ...
        """
        step = {}
        with io.StringIO(yaml_data) as f:
            read_yaml(f, step)
        self.assertEqual(step['Temperature'], 300)
        self.assertEqual(step['Pressure'], 1.0)
        self.assertEqual(step['Energy'], -1000)

    def test_read_yaml_nested_data(self):
        yaml_data = """---
        Forces:
          - [1.0, 2.0, 3.0]
          - [4.0, 5.0, 6.0]
        ...
        """
        step = {}
        with io.StringIO(yaml_data) as f:
            read_yaml(f, step)
        self.assertEqual(step['Forces'], [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

    def test_read_yaml_empty_value(self):
        yaml_data = """---
        Positions:
          -
            x: 1.0
            y: 2.0
            z:
          ...
        """
        step = {}
        with io.StringIO(yaml_data) as f:
            read_yaml(f, step)
        self.assertEqual(step['Positions'], [{'x': 1.0, 'y': 2.0, 'z': None}])

    def test_read_yaml_invalid_data(self):
        yaml_data = """---
        Temperature: abc
        Pressure: 1.0
        Energy: -1000.0
        ...
        """
        step = {}
        with io.StringIO(yaml_data) as f:
            read_yaml(f, step)
        self.assertEqual(step['Temperature'], 'abc')
        self.assertEqual(step['Pressure'], 1.0)
        self.assertEqual(step['Energy'], -1000)

    def test_read_yaml_no_data(self):
        yaml_data = ""
        step = {}
        with io.StringIO(yaml_data) as f:
            read_yaml(f, step)
        self.assertEqual(step, {})


if __name__ == '__main__':
    unittest.main()
