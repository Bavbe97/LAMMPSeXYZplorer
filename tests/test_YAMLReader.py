import unittest
import os
from unittest.mock import patch, MagicMock, mock_open
from lammpshade.YAMLReader import YAMLReader


class Test_YAMLReader_init_(unittest.TestCase):
    """
    Test the constructor of the YAMLReader class.
    """
    def test_init_file_not_found(self):
        """
        Test if the constructor raises a FileNotFoundError when the specified
        file is not found.

        Steps:
        1. Instantiate the YAMLReader class with a non-existent filename.
        2. Assert that a FileNotFoundError is raised.
        """

        with self.assertRaises(FileNotFoundError):
            # Instantiate the YAMLReader class with a non-existent filename
            YAMLReader("non_existent_file.yaml")


class Test_YAMLReader_convert_value(unittest.TestCase):
    """
    Tests the convert_value method of the YAMLReader class.
    """
    def test_convert_value_int(self):
        """
        Test if the convert_value method returns the corresponding integer
        value when called with an integer string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_value method with an integer string.
        3. Assert that the method returns the corresponding integer value.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with an integer string
        assert yaml_reader.convert_value("123") == 123
        assert yaml_reader.convert_value("-123") == -123

    def test_convert_value_float(self):
        """
        Test if the convert_value method returns the corresponding float value
        when called with a float string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_value method with a float string.
        3. Assert that the method returns the corresponding float value.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a float string
        assert yaml_reader.convert_value("3.14") == 3.14
        assert yaml_reader.convert_value("-3.14") == -3.14
        assert yaml_reader.convert_value("3.14e-2") == 3.14e-2
        assert yaml_reader.convert_value("-3.14e-2") == -3.14e-2
        assert yaml_reader.convert_value("3.14e2") == 3.14e2

    def test_convert_value_list_integers(self):
        """
        Test if the convert_value method returns a list of corresponding
        integer values when called with a list of integer strings.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_value method with a list of integer strings.
        3. Assert that the method returns a list of corresponding integer
           values.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a list of integer strings
        assert yaml_reader.convert_value("[1, 2, 3]") == [1, 2, 3]

    def test_convert_value_list_strings(self):
        """
        Test if the convert_value method returns a list of corresponding string
        values when called with a list of string strings.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_value method with a list of string strings.
        3. Assert that the method returns a list of corresponding string
           values.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a list of string strings
        assert yaml_reader.convert_value("[hello, world.]") == ['hello',
                                                                'world.']

    def test_convert_value_list_mixed(self):
        """
        Test if the convert_value method returns a list of corresponding
        integer, float, and string values when called with a list of mixed type
        strings.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_value method with a list of mixed type strings.
        3. Assert that the method returns a list of corresponding integer,
           float, and string values.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a list of mixed type strings
        assert yaml_reader.convert_value("[1, 2.5, hello]") == [1, 2.5,
                                                                'hello']


class Test_YAMLReader_convert_to_int(unittest.TestCase):
    """
    Tests the convert_to_int method of the YAMLReader class.
    """

    def test_convert_to_int_valid_integer(self):
        """
        Test if the input string is converted to an integer when it is a
        valid integer string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_int method with a valid integer string.
        3. Assert that the method returns the corresponding integer value.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        result = yaml_reader.convert_to_int("123")
        self.assertEqual(result, 123)

    def test_convert_to_int_negative_integer(self):
        """
        Test if the input string is converted to a negative integer when it is
        a valid negative integer string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_int method with a valid negative integer string.
        3. Assert that the method returns the corresponding negative integer
           value.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        result = yaml_reader.convert_to_int("-123")
        self.assertEqual(result, -123)

    def test_convert_to_int_invalid_integer(self):
        """
        Test if the input string is not converted to an integer when it is an
        invalid integer string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_int method with an invalid integer string.
        3. Assert that the method returns None.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        result = yaml_reader.convert_to_int("abc")
        self.assertIsNone(result)


class Test_YAMLReader_convert_to_float(unittest.TestCase):
    """
    Tests the convert_to_float method of the YAMLReader class.
    """
    def test_convert_to_float_valid_float(self):
        """
        Test if the input string is converted to a float when it is a
        valid float string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_float method with a valid float string.
        3. Assert that the method returns the corresponding float value.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        result = yaml_reader.convert_to_float("3.14")
        self.assertEqual(result, 3.14)

    def test_convert_to_float_negative_float(self):
        """
        Test if the input string is converted to a negative float when it is
        a valid negative float string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_float method with a valid negative float string.
        3. Assert that the method returns the corresponding negative float
           value.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        result = yaml_reader.convert_to_float("-3.14")
        self.assertEqual(result, -3.14)

    def test_convert_to_float_invalid_float(self):
        """
        Test if the input string is not converted to a float when it is an
        invalid float string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_float method with an invalid float string.
        3. Assert that the method returns None.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        result = yaml_reader.convert_to_float("abc")
        self.assertIsNone(result)

    def test_convert_to_float_invalid_float_format(self):
        """
        Test if the input string is not converted to a float when it is an
        invalid float string format.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_float method with an invalid float string
           format.
        3. Assert that the method returns None.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        result = yaml_reader.convert_to_float("3.14.15")
        self.assertIsNone(result)


class Test_YAMLReader_convert_to_list(unittest.TestCase):
    """
    Tests the convert_to_list method of the YAMLReader class.
    """

    def test_convert_to_list_valid_list(self):
        """
        Test if the convert_to_list method returns a list of corresponding
        elements when called with a valid list string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_list method with a valid list string.
        3. Assert that the method returns a list of corresponding elements.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_to_list method with a valid list string
        result = yaml_reader.convert_to_list("[1, 2, 3]")
        self.assertEqual(result, [1, 2, 3])

    def test_convert_to_list_empty_list(self):
        """
        Test if the convert_to_list method returns an empty list when called
        with an empty list string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_list method with an empty list string.
        3. Assert that the method returns an empty list.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_to_list method with an empty list string
        result = yaml_reader.convert_to_list("[]")
        self.assertEqual(result, [])

    def test_convert_to_list_invalid_list(self):
        """
        Test if the convert_to_list method returns None when called with an
        invalid list string.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the convert_to_list method with an invalid list string.
        3. Assert that the method returns None.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_to_list method with an invalid list string
        result = yaml_reader.convert_to_list("[1, 2, 3")
        self.assertIsNone(result)


class Test_YAMLReader_get_next_step(unittest.TestCase):
    """
    Tests the get_next_step method of the YAMLReader class.
    """
    def test_get_next_step_subsequent_key_value_pairs(self):
        """
        Test if the get_next_step method returns subsequent key-value pairs
        from the YAML file.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        natoms: 10
        units: real
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader("test_filename.yaml")
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['natoms'] == 10
            assert step['units'] == 'real'
            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_value_then_key_dictionaries(self):
        """
        Test if the get_next_step method returns a key-value pair and then a
        key-dictionary pair from the YAML file.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        natoms: 10
        thermo:
        - keywords: [ Step, Time, Quantity, ]
        - data: [ 0, 0, 300.01337588855796, ]
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
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
            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_value_then_key_lists(self):
        """
        Test if the get_next_step method returns a key-value pair and then a
        key-list pair from the YAML file.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        """

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
        # Configure the readline method of the mock file to return lines of
        # YAML content
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

    def test_get_next_step_key_dictionaries_then_key_lists(self):
        """
        Test if the get_next_step method returns a key-dictionary pair and then
        a key-list pair from the YAML file.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        """

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
        # Configure the readline method of the mock file to return lines of
        # YAML content
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

    def test_get_next_step_file_ends(self):
        """
        Test if the get_next_step method returns an empty dictionary when the
        YAML file ends.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        7. Call the get_next_step method again.
        8. Verify that the close method of the mock file object is called
           exactly once.
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader("test_filename.yaml")
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step == {}
            step = yaml_reader.get_next_step()

            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_lists_then_key_dictionaries(self):
        """
        Test if the get_next_step method returns subsequent key-list pairs and
        then a key-dictionary pair from the YAML file.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        """

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
        # Configure the readline method of the mock file to return lines of
        # YAML content
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

    def test_get_next_step_key_dictionaries_then_key_value(self):
        """
        Test if the get_next_step method returns a key-dictionary pair and then
        a key-value pair from the YAML file.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        thermo:
        - keywords: [ Step, Time, Quantity, Negative, Exponential, ]
        - data: [ 0, 0, 300.01337588855796, -26, -6.5e-3, ]
        natoms: 10
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader("test_filename.yaml")
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity',
                                                  'Negative', 'Exponential']
            assert step['thermo']['data'] == [0, 0, 300.01337588855796, -26,
                                              -6.5e-3]
            assert step['natoms'] == 10
            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_lists_then_key_value(self):
        """
        Test if the get_next_step method returns subsequent key-list pairs and
        then a key-value pair from the YAML file.

        Steps:
        1. Define YAML content to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Call the get_next_step method.
        6. Assert the expected behavior.
        """

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
        # Configure the readline method of the mock file to return lines of
        # YAML content
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

    def test_get_next_step_get_subsequent_step(self):
        """
        Test if the get_next_step method returns subsequent steps from the YAML
        file.

        Steps:
        1. Define YAML lines to simulate reading from a file.
        2. Create a mock file object.
        3. Configure the readline method of the mock file to return lines of
           YAML content.
        4. Patch the open function to return the mock file object.
        5. Instantiate the YAMLReader class with a fake filename.
        6. Call the get_next_step method until '...' is encountered.
        7. Assert the expected behavior.
        """

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


class Test_YAMLReader_process_key_value_pair(unittest.TestCase):
    """
    Tests the process_key_value_pair method of the YAMLReader class.
    """

    def test_process_key_value_pair(self):
        """
        Test if the method correctly processes a line containing a key-value
        pair.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_key_value_pair method with a line containing a
           key-value pair.
        3. Assert that the method returns the correct key and value.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "key: value"
        key, value = yaml_reader.process_key_value_pair(line)
        self.assertEqual(key, "key")
        self.assertEqual(value, "value")

    def test_process_key_value_pair_with_conversion(self):
        """
        Test if the method correctly processes a line containing a key-value
        pair with value conversion.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_key_value_pair method with a line containing a
           key-value pair with value conversion.
        3. Assert that the method returns the correct key and converted value.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "key: 123"
        key, value = yaml_reader.process_key_value_pair(line)
        self.assertEqual(key, "key")
        self.assertEqual(value, 123)

    def test_process_key_no_value(self):
        """
        Test if the method correctly processes a line containing a key without
        a value.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_key_value_pair method with a line containing a
           key without a value.
        3. Assert that the method returns the correct key and an empty string.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "key:"
        key, value = yaml_reader.process_key_value_pair(line)
        self.assertEqual(key, "key")
        self.assertFalse(value)


class Test_YAMLReader_process_list(unittest.TestCase):
    """
    Tests the process_list method of the YAMLReader class.
    """

    def test_process_list_single_element(self):
        """
        Test if the process_list method returns a list with a single element
        when called with a line containing a single element.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_list method with a line containing a single
        element.
        3. Assert that the method returns a list with the single element.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "- element1\n"
        expected_result = ['element1']
        result, _ = yaml_reader.process_list(line)
        self.assertEqual(result, expected_result)

    def test_process_list_empty_line(self):
        """
        Test if the process_list method returns an empty list when called with
        an empty line.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_list method with an empty line.
        3. Assert that the method returns an empty list.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "\n"
        expected_result = []
        result, _ = yaml_reader.process_list(line)
        self.assertEqual(result, expected_result)

    def test_process_list_no_elements(self):
        """
        Test if the process_list method returns an empty list when called with
        a line containing no elements.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_list method with a line containing no elements.
        3. Assert that the method returns an empty list.
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "-\n"
        expected_result = []
        result, _ = yaml_reader.process_list(line)
        self.assertEqual(result, expected_result)


class Test_YAMLReader_process_dictionary(unittest.TestCase):
    """
    Tests the process_dictionary method of the YAMLReader class.
    """

    def test_process_dictionary_single_element(self):
        """
        Test if the process_dictionary method correctly processes a line
        containing a single element dictionary.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_dictionary method with a line containing a single
           element dictionary.
        3. Assert that the method returns a dictionary with the correct key and
           value.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "- key: value\n"
        expected_result = {'key': 'value'}
        result, next_line = yaml_reader.process_dictionary(line)
        self.assertEqual(result, expected_result)
        self.assertEqual(next_line, '---\n')

    def test_process_dictionary_empty_line(self):
        """
        Test if the process_dictionary method correctly handles an empty line.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_dictionary method with an empty line.
        3. Assert that the method returns an empty dictionary and an empty
           string as the next line.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = ''
        expected_result = {}
        result, next_line = yaml_reader.process_dictionary(line)
        self.assertEqual(result, expected_result)
        self.assertEqual(next_line, '')

    def test_process_dictionary_no_elements(self):
        """
        Test if the process_dictionary method correctly handles a line with no
        elements.

        Steps:
        1. Instantiate the YAMLReader class.
        2. Call the process_dictionary method with a line with no elements.
        3. Assert that the method returns an empty dictionary and the same line
           as the next line.
        """
        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        line = "- \n"
        expected_result = {}
        result, next_line = yaml_reader.process_dictionary(line)
        self.assertEqual(result, expected_result)
        self.assertEqual(next_line, line)


if __name__ == '__main__':
    unittest.main()
