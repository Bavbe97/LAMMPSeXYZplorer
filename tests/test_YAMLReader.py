# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:09:24 2024

@author: fbarb
"""

import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
from lammpshade.YAMLReader import YAMLReader




yaml_content = """---
units: real
timestep: 1
temperature: 300
forcefield: Amber
...
"""


def test_convert_value_int():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("123") == 123


def test_convert_value_float():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("3.14") == 3.14


def test_convert_value_list_integers():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("[1, 2, 3]") == [1, 2, 3]


def test_convert_value_list_mixed():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("[1, 2.5, hello]") == [1, 2.5, 'hello']


def test_get_next_step():
    # Define YAML content to simulate reading from a file
    yaml_content = """---
    units: real
    timestep: 1
    temperature: 300
    forcefield: Amber
    ..."""
    # Create a mock file object
    mock_file = MagicMock()
    # Configure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        # Instantiate the YAMLReader class with a fake filename
        yaml_reader = YAMLReader("fake_filename.yaml")
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behavior
        assert step['units'] == 'real'
        assert step['timestep'] == 1
        assert step['temperature'] == 300
        assert step['forcefield'] == 'Amber'
        # Verify that the close method of the mock file object is called exactly once
        mock_file.close.assert_called_once()
        


def test_get_units_real():
    yaml_reader = YAMLReader(None)
    yaml_reader.current_step = {'units': 'real'}
    assert yaml_reader.get_units('Time') == '(fs)'
    assert yaml_reader.get_units('velocity') == r'($\AA$ / fs)'
    assert yaml_reader.get_units('force') == r'(kCal/(mol - $\AA$))'
    assert yaml_reader.get_units('temperature') == '(K)'
    assert yaml_reader.get_units('other') == ''


if __name__ == '__main__':
    unittest.main()
