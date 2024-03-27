# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:09:24 2024

@author: fbarb
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
from lammpshade.YAMLReader import YAMLReader


def test_convert_value_int():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("123") == 123


def test_convert_value_float():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("3.14") == 3.14


def test_convert_value_list_integers():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("[1, 2, 3]") == [1, 2, 3]


def test_convert_value_list_strings():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("[hello, world.]") == ['hello', 'world.']


def test_convert_value_list_mixed():
    yaml_reader = YAMLReader(None)
    assert yaml_reader.convert_value("[1, 2.5, hello]") == [1, 2.5, 'hello']


def test_get_next_step_subsequent_key_value_pairs():
    # Define YAML content to simulate reading from a file
    yaml_content = '''---
    natoms: 10
    units: real
    ...'''
    # Create a mock file object
    mock_file = MagicMock()
    # Configure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader("test_filename.yaml")
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step['natoms'] == 10
        assert step['units'] == 'real'
        # Verify that the close method of the mock file object is called exactly once
        mock_file.close.assert_called_once()


def test_get_next_step_key_value_then_key_dictionaries():
    # Define YAML content to simulate reading from a file
    yaml_content = '''---
    natoms: 10
    thermo:
      - keywords: [ Step, Time, Quantity, ]
      - data: [ 0, 0, 300.01337588855796, ]
    ...'''
    # Create a mock file object
    mock_file = MagicMock()
    # Configure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']
    
    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader("test_filename.yaml")
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step['natoms'] == 10
        assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity']
        assert step['thermo']['data'] == [0, 0, 300.01337588855796]
        # Verify that the close method of the mock file object is called exactly once
        mock_file.close.assert_called_once()


def test_get_next_step_key_value_then_key_lists():
    # Define YAML content to simulate reading from a file
    yaml_content = '''---
    natoms: 10
    box:
      - [ 0, 53 ]
      - [ 0, 52.57 ]
      - [ 0.439, 96.33 ]
    ...'''
    # Create a mock file object
    mock_file = MagicMock()
    # Configure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader('test_filename.yaml')
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step['natoms'] == 10
        assert step['box'] == [[0, 53],
                               [0, 52.57],
                               [0.439, 96.33]]


def test_get_next_step_key_dictionaries_then_key_lists():
    # Define YAML content to simulate reading from a file
    yaml_content = '''---
    thermo:
      - keywords: [ Step, Time, Quantity, ]
      - data: [ 0, 0, 300.01337588855796, ]
    box:
      - [ 0, 53 ]
      - [ 0, 52.57 ]
      - [ 0.439, 96.33 ]
    ...'''
    # Create a mock file object
    mock_file = MagicMock()
    # COnfigure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader('test_filename.yaml')
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity']
        assert step['thermo']['data'] == [0, 0, 300.01337588855796]
        assert step['box'] == [[0, 53],
                               [0, 52.57],
                               [0.439, 96.33]]


def test_get_next_step_file_ends():
    # Define YAML content to simulate reading from a file
    yaml_content = '''...'''
    # Create a mock file object
    mock_file = MagicMock()
    # Configure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader("test_filename.yaml")
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step == {}
        
        step = yaml_reader.get_next_step()
        
        # Verify that the close method of the mock file object is called exactly once
        mock_file.close.assert_called_once()


def test_get_next_step_key_lists_then_key_dictionaries():
    # Define YAML content to simulate reading from a file
    yaml_content = '''---
    box:
      - [ 0, 53 ]
      - [ 0, 52.57 ]
      - [ 0.439, 96.33 ]
      thermo:
        - keywords: [ Step, Time, Quantity, ]
        - data: [ 0, 0, 300.01337588855796, ]
    ...'''
    # Create a mock file object
    mock_file = MagicMock()
    # COnfigure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader('test_filename.yaml')
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step['box'] == [[0, 53],
                               [0, 52.57],
                               [0.439, 96.33]]
        assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity']
        assert step['thermo']['data'] == [0, 0, 300.01337588855796]


def test_get_next_step_key_dictionaries_then_key_value():
    # Define YAML content to simulate reading from a file
    yaml_content = '''---
    thermo:
      - keywords: [ Step, Time, Quantity, ]
      - data: [ 0, 0, 300.01337588855796, ]
    natoms: 10
    ...'''
    # Create a mock file object
    mock_file = MagicMock()
    # Configure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader("test_filename.yaml")
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity']
        assert step['thermo']['data'] == [0, 0, 300.01337588855796]
        assert step['natoms'] == 10
        # Verify that the close method of the mock file object is called exactly once
        mock_file.close.assert_called_once()


def test_get_next_step_key_lists_then_key_value():
    # Define YAML content to simulate reading from a file
    yaml_content = '''---
    box:
      - [ 0, 53 ]
      - [ 0, 52.57 ]
      - [ 0.439, 96.33 ]
    natoms: 10
    ...'''
    # Create a mock file object
    mock_file = MagicMock()
    # Configure the readline method of the mock file to return lines of YAML content
    mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

    # Patch the open function to return the mock file object
    with patch('builtins.open', return_value=mock_file):
        yaml_reader = YAMLReader('test_filename.yaml')
        # Call the get_next_step method
        step = yaml_reader.get_next_step()
        # Assert the expected behaviour
        assert step['box'] == [[0, 53],
                               [0, 52.57],
                               [0.439, 96.33]]
        assert step['natoms'] == 10


def test_get_next_step_get_subsequent_step():
    # Define YAML lines to simulate reading from a file
    yaml_lines = [
        "---",
        "natoms: 10",
        "...",
        "---",
        "creator: LAMMPS",
        "box:",
        "  - [ 0, 53 ]",
        "  - [ 0, 52.57 ]",
        "  - [ 0.439, 96.33 ]",
        "..."
    ]
    
    # Create a mock file object
    mock_file = mock_open(read_data='\n'.join(yaml_lines))
    
    # Patch the open function to return the mock file object
    with patch('builtins.open', mock_file):
        # Instantiate the YAMLReader class with a fake filename
        yaml_reader = YAMLReader("fake_filename.yaml")
        
        # Call the get_next_step method until '...' is encountered
        step = yaml_reader.get_next_step()
        step = yaml_reader.get_next_step()
        
        # Assert the expected behavior
        assert 'natoms' not in step
        assert step['creator'] == 'LAMMPS'
        assert step['box'] == [[0, 53], [0, 52.57], [0.439, 96.33]]


if __name__ == '__main__':
    unittest.main()
