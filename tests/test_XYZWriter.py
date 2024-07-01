import unittest
from lammpshade.XYZWriter import XYZWriter
import os
import tempfile
import pandas as pd


class Test_XYZWriter_init_(unittest.TestCase):
    """
    Test the __init__ method of the XYZWriter class.
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
        working directory.

        Check if the files already exists and delete them if they do.
        Check if the 'output' directory exists and delete it if it's empty.
        Assert that the files do not exist.
        """
        self.created_files = []
        filenames = ["test_output.xyz", "existing_file.xyz", "new_file.xyz"]
        for filename in filenames:
            self.created_files.append(os.path.join(os.getcwd(), 'xyz',
                                      filename))

        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

        for file_path in self.created_files:
            assert not os.path.exists(file_path)

    def tearDown(self):
        """
        Remove the files created during testing.
        Remove the 'output' directory if it's empty.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_file_endswith_xyz(self):
        """
        Test if the file given to initialize the class ends with something
        other than '.xyz'.

        The expected behavior is to raise a ValueError.

        Steps:
        1. Create a file with a name that does not end with '.xyz'.
        2. Initialize the XYZWriter class with the file.
        3. Check if a ValueError is raised.

        """
        with self.assertRaises(ValueError):
            XYZWriter("example.txt")

    def test_file_created_in_output_directory(self):
        """
        Test if the file is created in the './xyz/' directory.
        The expected behavior is to create the file in the 'xyz' directory.
        If the directory does not exist, it should be created.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Check if the file is created in the './xyz/' directory.
        3. Check if the file is writable.
        """
        filename = "test_output.xyz"

        output = XYZWriter(filename)
        with output as out:
            self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'xyz',
                                                        filename)))
            self.assertTrue(out.output.writable())

    def test_file_already_exists(self):
        """
        Test if the file already exists and is opened.
        The expected behavior is to open the file for writing.

        Steps:
        1. Create a file with some content.
        2. Initialize the XYZWriter class with the filename.
        3. Check if the file is opened for writing.
        4. Check if the file is writable.
        """
        # Test if the file already exists and is opened
        filename = "existing_file.xyz"
        file_path = os.path.join(os.getcwd(), 'xyz', filename)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write("existing content")
        output = XYZWriter(filename)
        with output:
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(output.output.writable())

    def test_file_not_exists(self):
        """
        Test if the file does not exist and is created.
        The expected behavior is to create the file.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Check if the file is created.
        3. Check if the file is writable.
        """
        # Test if the file is created if it does not exist
        filename = "new_file.xyz"
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        output = XYZWriter(filename)
        with output:
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(output.output.writable())

    def test_create_file_in_different_filepath(self):
        """
        Test if the file is created in a different directory.
        The expected behavior is to create the file in the specified directory.

        Steps:
        1. Create a temporary directory.
        2. Initialize the XYZWriter class with a filename and the temporary
           directory.
        3. Check if the file is created in the specified directory.
        4. Check if the file is writable.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = "different_filepath.xyz"
            full_filepath = os.path.join(temp_dir, filename)
            out = XYZWriter(full_filepath)
            with out as out:
                self.assertTrue(os.path.exists(full_filepath))
                self.assertTrue(out.output.writable())

                # Check if the file is created in the correct directory
                self.assertTrue(full_filepath.startswith(temp_dir))
                self.created_files.append(full_filepath)


class Test_XYZWriter_write_to_xyz(unittest.TestCase):
    """
    Test the write_to_xyz method of the XYZWriter class.
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
            working directory.

        Check if the files already exists and delete them if they do.
        Check if the 'output' directory exists and delete it if it's empty.
        Assert that the files do not exist.
        """
        self.created_files = []
        filename = "test.xyz"
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

        for file_path in self.created_files:
            assert not os.path.exists(file_path)

    def tearDown(self):
        """
        Remove the files created during testing.
        Remove the 'output' directory if it's empty.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_write_to_xyz(self):
        """
        Test if the data is written to the file in the correct format.
        The expected behavior is to write the data to the file in the correct
        format. The data should be written in the format:
        natoms
        comment
        id type mass element x y z vx vy vz fx fy fz
        id type mass element x y z vx vy vz fx fy fz
        ...

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write data to the file.
        3. Check if the data is written to the file in the correct format.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': 10, 'keywords': ['id', 'type', 'mass', 'element',
                                           'x', 'y', 'z', 'vx', 'vy', 'vz',
                                           'fx', 'fy', 'fz'],
                'data': [[1, 2, 12, 'H2', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0],
                         [2, 3, 16, 'C3', 0.3, 0.31, 0.4, 5,  0.6, 77, -88.8,
                          'test', 0],
                         [3, 0, 32, 'N', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0]]
                }
        with out as out:
            out.write_to_xyz(step)
        with open(file_path, 'r') as file:
            content = file.readlines()
        self.assertIn('10\n', content)
        self.assertIn('H2 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 2\n', content)
        self.assertIn('C3 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 3\n', content)
        self.assertIn('N 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 0\n', content)

    def test_no_data(self):
        """
        Test if the data is not provided.
        The expected behavior is to raise a KeyError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write data to the file without providing the data.
        3. Check if a KeyError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': 10, 'keywords': ['id', 'type', 'mass', 'element',
                                           'x', 'y', 'z', 'vx', 'vy', 'vz',
                                           'fx', 'fy', 'fz']}
        with self.assertRaises(KeyError):
            out.write_to_xyz(step)

    def test_no_atoms(self):
        """
        Test if the number of atoms is not provided.
        The expected behavior is to raise a KeyError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write data to the file without providing the atoms data.
        3. Check if a KeyError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        data = {'natoms': 10}
        with self.assertRaises(KeyError):
            out.write_to_xyz(data)

    def test_no_element_coordinates(self):
        """
        Test if the necessary element coordinates are not provided.
        The necessary element coordinates are: 'element', 'x', 'y', 'z'.
        The expected behavior is to raise a KeyError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write data to the file without providing the element coordinates.
        3. Check if a KeyError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': 10, 'keywords': ['id', 'type', 'mass', 'vx', 'vy',
                                           'vz', 'fx', 'fy', 'fz'],
                'data': [[1, 2, 12, 5, 0.6, 77, -88.8, 'test', 0],
                         [2, 3, 16, 5, 0.6, 77, -88.8, 'test', 0],
                         [3, 0, 32, 5, 0.6, 77, -88.8, 'test', 0]]
                }
        with self.assertRaises(KeyError):
            out.write_to_xyz(step)

    def test_thermo_data_no_box(self):
        """
        Test if the thermo data is provided without the box data.
        The expected behavior is to write the thermo data to the file in the
        correct format without the box data.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write data to the file with the thermo data.
        3. Check if the data is written to the file in the correct format.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        output = XYZWriter(file_path)
        step = {'natoms': 10, 'thermo': {'keywords':
                                         ['Step', 'Time', 'c_temp', 'v_vel',
                                          'v_force', 'test'],
                                         'data': [0, 1, 6, -11.3, 999, 'test']
                                         },
                'keywords': ['id', 'type', 'mass', 'element', 'x', 'y', 'z',
                             'vx', 'vy', 'vz', 'fx', 'fy', 'fz'],
                'data': [[1, 2, 12, 'H2', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0],
                         [2, 3, 16, 'C3', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0],
                         [3, 0, 32, 'N', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0]]
                }
        with output as out:
            out.write_to_xyz(step)
        with open(file_path, 'r') as file:
            content = file.readlines()
        self.assertIn('10\n', content)
        self.assertIn('Step=0; Time=1; temp=6; vel=-11.3; force=999; '
                      'test=test\n', content)
        self.assertIn('H2 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 2\n', content)
        self.assertIn('C3 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 3\n', content)
        self.assertIn('N 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 0\n', content)

    def test_thermo_data_yes_box(self):
        """
        Test if the thermo data is provided with the box data.
        The expected behavior is to write the thermo data to the file in the
        correct format with the box data.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write data to the file with the thermo data.
        3. Check if the data is written to the file in the correct format.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        output = XYZWriter(file_path)
        step = {'natoms': 10, 'box': [[0, 5], [0, 0], [4.7, -9]],
                'thermo': {'keywords': ['Step', 'Time', 'c_temp', 'v_vel',
                                        'v_force', 'test'],
                           'data': [0, 1, 6, -11.3, 999, 'test']},
                'keywords': ['id', 'type', 'mass', 'element', 'x', 'y', 'z',
                             'vx', 'vy', 'vz', 'fx', 'fy', 'fz'],
                'data': [[1, 2, 12, 'H2', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0],
                         [2, 3, 16, 'C3', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0],
                         [3, 0, 32, 'N', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0]]
                }
        with output as out:
            out.write_to_xyz(step)
        with open(file_path, 'r') as file:
            content = file.readlines()
        self.assertIn('10\n', content)
        self.assertIn('Step=0; Time=1; Box=[0, 5], [0, 0], [4.7, -9]; temp=6; '
                      'vel=-11.3; force=999; test=test\n', content)
        self.assertIn('H2 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 2\n', content)
        self.assertIn('C3 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 3\n', content)
        self.assertIn('N 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 0\n', content)


class Test_XYZWriter_process_and_write_natoms(unittest.TestCase):
    """
    Test the write_natoms method of the XYZWriter class.
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
        working directory.

        Check if the files already exists and delete them if they do.
        Check if the 'output' directory exists and delete it if it's empty.
        Assert that the files do not exist.
        """
        self.created_files = []
        filename = "test.xyz"
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

        for file_path in self.created_files:
            assert not os.path.exists(file_path)

    def tearDown(self):
        """
        Remove the files created during testing.
        Remove the 'output' directory if it's empty.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_write_natoms(self):
        """
        Test if the number of atoms is written to the file in the correct
        format.
        The expected behavior is to write the number of atoms in a single line.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the number of atoms to the file.
        3. Check if the number of atoms is written to the file in the correct
           format.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': 10}
        with out as out:
            out.process_and_write_natoms(step)
        with open(file_path, 'r') as file:
            content = file.readlines()
        self.assertIn('10\n', content)

    def test_no_natoms(self):
        """
        Test if the number of atoms is not provided.
        The expected behavior is to raise a KeyError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the number of atoms to the file without providing the number
           of atoms.
        3. Check if a KeyError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {}
        with out as out:
            with self.assertRaises(KeyError):
                out.process_and_write_natoms(step)

    def test_list_natoms(self):
        """
        Test if the number of atoms is provided as a list.
        The expected behavior is to raise a TypeError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the number of atoms to the file as a list.
        3. Check if a TypeError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': [10]}
        with out as out:
            with self.assertRaises(TypeError):
                out.process_and_write_natoms(step)

    def test_string_natoms(self):
        """
        Test if the number of atoms is provided as a string.
        The expected behavior is to raise a TypeError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the number of atoms to the file as a string.
        3. Check if a TypeError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': '10'}
        with out as out:
            with self.assertRaises(TypeError):
                out.process_and_write_natoms(step)

    def test_float_natoms(self):
        """
        Test if the number of atoms is provided as a float.
        The expected behavior is to raise a TypeError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the number of atoms to the file as a float.
        3. Check if a TypeError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': 10.546}
        with out as out:
            with self.assertRaises(TypeError):
                out.process_and_write_natoms(step)

    def test_negative_natoms(self):
        """
        Test if the number of atoms is provided as a negative integer.
        The expected behavior is to raise a TypeError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the number of atoms to the file as a negative integer.
        3. Check if a ValueError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': -10}
        with out as out:
            with self.assertRaises(TypeError):
                out.process_and_write_natoms(step)


class Test_XYZWriter_process_thermo_data(unittest.TestCase):
    """
    Test the process_thermo_data method of the XYZWriter class.
    """

    def test_no_thermodata(self):
        """
        Test if the thermo data is not provided.
        The expected behavior is to set thermo_check[0] as false and print
        a warning.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the thermo data without providing the thermo data.
        3. Check if thermo_check[0] is set as false.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {}
        thermo_check, thermo_data = out.process_thermo_data(step)

        self.assertFalse(thermo_check[0])
        self.assertEqual(thermo_data, "")

    def test_thermodata(self):
        """
        Test if the thermo data is provided.
        The expected behavior is to set thermo_check[0] as true and return the
        thermo data processed.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the thermo data.
        3. Check if thermo_check[0] is set as true.
        4. Check if the thermo data is returned.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'thermo': {'keywords': ['Step', 'Time', 'c_temp', 'v_vel',
                                        'v_force', 'test'],
                           'data': [0, 1, 6, -11.3, 999, 'test']}
                }
        thermo_check, thermo_data = out.process_thermo_data(step)
        self.assertTrue(thermo_check[0])
        self.assertEqual(thermo_data, "Step=0; Time=1; temp=6; vel=-11.3; " +
                         "force=999; test=test")


class Test_XYZWriter_write_thermo_data(unittest.TestCase):
    """
    Test the write_thermo_data method of the XYZWriter class.
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
        working directory.

        Check if the files already exists and delete them if they do.
        Check if the 'output' directory exists and delete it if it's empty.
        Assert that the files do not exist.
        """
        self.created_files = []
        filename = "test.xyz"
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

        for file_path in self.created_files:
            assert not os.path.exists(file_path)

    def tearDown(self):
        """
        Remove the files created during testing.
        Remove the 'output' directory if it's empty.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_no_thermodata(self):
        """
        Test if the thermo data is not provided.
        The expected behavior is to print an empty line in the file.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the thermo data to the file without providing the thermo data.
        3. Check if an empty line is written to the file.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {}
        thermo_check, thermo_data = out.process_thermo_data(step)
        with out as out:
            out.write_thermo_data(thermo_data)
        with open(file_path, 'r') as file:
            content = file.readlines()
            self.assertIn('\n', content)

    def test_thermodata(self):
        """
        Test if the thermo data is provided.
        The expected behavior is to write the thermo data to the file in the
        correct format.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the thermo data to the file.
        3. Check if the thermo data is written to the file in the correct
           format.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'thermo': {'keywords': ['Step', 'Time', 'c_temp', 'v_vel',
                                        'v_force', 'test'],
                           'data': [0, 1, 6, -11.3, 999, 'test']}
                }
        thermo_check, thermo_data = out.process_thermo_data(step)
        with out as out:
            out.write_thermo_data(thermo_data)
        with open(file_path, 'r') as file:
            content = file.readlines()
        self.assertIn(thermo_data + '\n', content)


class Test_XYZWriter_process_box_data(unittest.TestCase):
    """
    Test the process_box_data method of the XYZWriter class.
    """
    def test_no_box_data(self):
        """
        Test if the box data is not provided.
        The expected behavior is to set thermo_check[1] as false and print a
        warning.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the box data without providing the box data.
        3. Check if box_check[0] is set as false.
        """
        filename = 'test1.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {}
        thermo_check, thermo_data = out.process_box_data(step, thermo_data="")

        self.assertFalse(thermo_check[1])
        self.assertEqual(thermo_data, "")

    def test_thermo_data_no_box(self):
        """
        Test if the thermo data is provided without the box data.
        The expected behavior is to set thermo_check[1] as false and print a
        warning.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the box data without providing the box data.
        3. Check if thermo_check[1] is set as false.
        """
        filename = 'test1.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'thermo': {'keywords': ['Step', 'Time', 'c_temp', 'v_vel',
                                        'v_force', 'test'],
                           'data': [0, 1, 6, -11.3, 999, 'test']}
                }
        thermo_check, thermo_data = out.process_box_data(step, thermo_data="")
        self.assertFalse(thermo_check[1])
        self.assertEqual(thermo_data, "")

    def test_box_data(self):
        """
        Test if the box data is provided.
        The expected behavior is to set thermo_check[1] as true and return the
        box data processed.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the box data.
        3. Check if thermo_check[1] is set as true.
        4. Check if the box data is returned.
        """
        filename = 'test2.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'box': [[0, 5], [0, 0], [4.7, -9]]}
        thermo_data = "Step=0; Time=1; temp=6; vel=-11.3; force=999; test=test"
        thermo_check, thermo_data = out.process_box_data(step, thermo_data)
        self.assertTrue(thermo_check[1])
        self.assertEqual(thermo_data, "Step=0; Time=1; Box=[0, 5], [0, 0], " +
                         "[4.7, -9]; temp=6; vel=-11.3; force=999; test=test")

    def test_bad_formatted_thermo_data(self):
        """
        Test if the thermo data is provided in a bad format.
        The expected behavior is to set thermo_check[i] = False and continue
        without writing thermo_data.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the box data with the thermo data in a bad format.
        3. Check if thermo_check[0] is set as false.
        4. Check if thermo_check[1] is set as false.
        """
        filename = 'test3.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'box': [[0, 5], [0, 0], [4.7, -9]]}
        thermo_data = "Step=0; Tim=1; temp=6; vel=-11.3; force=999; test=test"
        thermo_check, thermo_data = out.process_box_data(step, thermo_data)
        self.assertFalse(thermo_check[0])
        self.assertFalse(thermo_check[1])


class Test_XYZWrite_process_and_write_thermodata(unittest.TestCase):
    """
    Test the process_and_write_thermo_data method of the XYZWriter class.
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
        working directory.

        Check if the files already exists and delete them if they do.
        Check if the 'output' directory exists and delete it if it's empty.
        Assert that the files do not exist.
        """
        self.created_files = []
        filenames = ['test.xyz']
        for filename in filenames:
            self.created_files.append(os.path.join(os.getcwd(), 'xyz',
                                      filename))

        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

        for file_path in self.created_files:
            assert not os.path.exists(file_path)

    def tearDown(self):
        """
        Remove the files created during testing.
        Remove the 'output' directory if it's empty.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_no_thermodata(self):
        """
        Test if the thermo data is not provided.
        The expected behavior is to print an empty line in the file.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the thermo data to the file without providing the thermo data.
        3. Check if an empty line is written to the file.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {}
        with out as out:
            out.process_and_write_thermo_data(step)
        with open(file_path, 'r') as file:
            content = file.readlines()
            self.assertIn('\n', content)

    def test_thermodata(self):
        """
        Test if the thermo data is provided.
        The expected behavior is to write the thermo data to the file in the
        correct format.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the thermo data to the file.
        3. Check if the thermo data is written to the file in the correct
           format.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'thermo': {'keywords': ['Step', 'Time', 'c_temp', 'v_vel',
                                        'v_force', 'test'],
                           'data': [0, 1, 6, -11.3, 999, 'test']}
                }
        with out as out:
            out.process_and_write_thermo_data(step)
        with open(file_path, 'r') as file:
            content = file.readlines()
        self.assertIn('Step=0; Time=1; temp=6; vel=-11.3; force=999; '
                      'test=test\n', content)


class Test_XYZWriter_process_atom_data_df(unittest.TestCase):
    """
    Test the process_atom_data_df method of the XYZWriter class.
    """
    def test_no_atom_df(self):
        """
        Test if the atom data is not provided.
        The expected behavior is to raise a TypeError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the atom data without providing the atom data.
        3. Check if a KeyError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        with self.assertRaises(TypeError):
            out.process_atom_data_df()

    def test_empty_atom_df(self):
        """
        Test if the atom data is an empty DataFrame.
        The expected behavior is to return the empty DataFrame.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the atom data with an empty DataFrame.
        3. Check if the empty DataFrame is returned.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        atom_df = pd.DataFrame()
        processed_atom_df = out.process_atom_data_df(atom_df)
        self.assertTrue(processed_atom_df.empty)

    def test_atom_df_more_keywords(self):
        """
        Test if the atom data has more keywords than the filter ones.
        The expected behavior is to return the DataFrame with only the filtered
        keywords.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the atom data with more keywords than the filter ones.
        3. Check if the DataFrame with only the filtered keywords is returned.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        atom_df = pd.DataFrame(columns=['id', 'type', 'mass', 'element', 'x',
                                        'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy',
                                        'fz', 'extra'])
        processed_atom_df = out.process_atom_data_df(atom_df)
        self.assertListEqual(list(processed_atom_df.columns), ['element', 'x',
                                                               'y', 'z', 'vx',
                                                               'vy', 'vz',
                                                               'fx', 'fy',
                                                               'fz', 'type'])

    def test_atom_df_less_keywords(self):
        """
        Test if the atom data has less keywords than the filter ones.
        The expected behavior is to return the DataFrame with only the filtered
        keywords that are present in the atom data.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Process the atom data with less keywords than the filter ones.
        3. Check if the DataFrame with only the filtered keywords is returned.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        atom_df = pd.DataFrame(columns=['id', 'type', 'element', 'x', 'y', 'z',
                                        'vx'])
        processed_atom_df = out.process_atom_data_df(atom_df)
        self.assertListEqual(list(processed_atom_df.columns), ['element', 'x',
                                                               'y', 'z', 'vx',
                                                               'type'])


class Test_XYZWriter_create_and_write_atom_data(unittest.TestCase):
    """
    Test the create_and_write_atom_data method of the XYZWriter class.
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
        working directory.

        Check if the files already exists and delete them if they do.
        Check if the 'output' directory exists and delete it if it's empty.
        Assert that the files do not exist.
        """
        self.created_files = []
        filenames = ['test.xyz']
        for filename in filenames:
            self.created_files.append(os.path.join(os.getcwd(), 'xyz',
                                      filename))

        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

        for file_path in self.created_files:
            assert not os.path.exists(file_path)

    def tearDown(self):
        """
        Remove the files created during testing.
        Remove the 'output' directory if it's empty.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_no_atom_df(self):
        """
        Test if the atom data is not provided.
        The expected behavior is to raise a TypeError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the atom data to the file without providing the atom data.
        3. Check if a TypeError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        with self.assertRaises(TypeError):
            out.create_and_write_atom_data()

    def test_empty_atom_df(self):
        """
        Test if the atom data is an empty DataFrame.
        The expected behavior is to raise a KeyError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the atom data to the file with an empty DataFrame.
        3. Check if a KeyError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        atom_df = pd.DataFrame()
        with self.assertRaises(KeyError):
            with out as out:
                out.create_and_write_atom_data(atom_df)

    def test_atom_df(self):
        """
        Test if the atom data is provided.
        The expected behavior is to write the atom data to the file in the
        correct format.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Write the atom data to the file.
        3. Check if the atom data is written to the file in the correct format.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)

        step = {'keywords': ['id', 'type', 'mass', 'element', 'x', 'y', 'z',
                             'vx', 'vy', 'vz', 'fx', 'fy', 'fz'],
                'data': [[1, 2, 12, 'H2', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0],
                         [2, 3, 16, 'C3', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0],
                         [3, 0, 32, 'N', 0.3, 0.31, 0.4, 5, 0.6, 77, -88.8,
                          'test', 0]]}

        with out as out:
            out.create_and_write_atom_data(step)
        with open(file_path, 'r') as file:
            content = file.readlines()
        self.assertIn('H2 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 2\n', content)
        self.assertIn('C3 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 3\n', content)
        self.assertIn('N 0.3 0.31 0.4 5 0.6 77 -88.8 test 0 0\n', content)


class Test_XYZWriter_data_check(unittest.TestCase):
    """
    Test the data_check method of the XYZWriter class.
    """
    def test_no_data(self):
        """
        Test if the data is not provided.
        The expected behavior is to raise a TypeError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Check the data without providing the data.
        3. Check if a TypeError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        with self.assertRaises(TypeError):
            out.data_check()

    def test_missing_key(self):
        """
        Test if the data is missing a key.
        The expected behavior is to raise a KeyError.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Check the data without providing a key.
        3. Check if a KeyError is raised.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {}
        keys = ['test']
        with self.assertRaises(KeyError):
            out.data_check(step, keys, 'test')

    def test_all_keys(self):
        """
        Test if all the keys are provided.
        The expected behaviour is to pass the data check.

        Steps:
        1. Initialize the XYZWriter class with a filename.
        2. Check the data with all the keys provided.
        3. Check if the data check passes.
        """
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'keywords': 'test', 'data': 'test'}
        keys = ['keywords', 'data']
        check = out.data_check(step, keys, 'test')
        self.assertTrue(check)


class Test_XYZWriter_contest_manager(unittest.TestCase):
    """
    Test the context manager of the XYZWriter class.
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
        working directory.
        """
        self.created_files = []

    def tearDown(self):
        """
        Remove the files created during testing.
        Remove the 'output' directory if it's empty.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_enter(self):
        """
        Test if the file is created and opened for writing.
        The expected behavior is to create the file and open it for writing.

        Steps:
        1. Create a temporary directory.
        2. Initialize the XYZWriter class with a filename and the temporary
           directory.
        3. Check if the file is created and opened for writing.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = 'test.xyz'
            file_path = os.path.join(temp_dir, filename)
            self.created_files.append(file_path)
            output = XYZWriter(file_path)
            with output as out:
                self.assertTrue(os.path.exists(file_path))
                self.assertTrue(out.output.writable())

    def test_exit(self):
        """
        Test if the file is closed after writing.
        The expected behavior is to close the file after writing.

        Steps:
        1. Create a temporary directory.
        2. Initialize the XYZWriter class with a filename and the temporary
           directory.
        3. Write data to the file.
        4. Check if the file is closed after writing.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = 'test.xyz'
            file_path = os.path.join(temp_dir, filename)
            self.created_files.append(file_path)
            output = XYZWriter(file_path)
            with output:
                pass
        self.assertFalse(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
