import unittest
from lammpshade.XYZWriter import XYZWriter
import os
import tempfile


class Test_XYZWriter_init_(unittest.TestCase):
    """
    Test the __init__ method of the XYZWriter class.
    """

    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the 'xyz' directory in the current
        working directory.

        Check if the files already exist and raise an error if they do.
        """
        self.created_files = []
        filenames = ["test_output.xyz", "existing_file.xyz", "new_file.xyz"]
        for filename in filenames:
            self.created_files.append(os.path.join(os.getcwd(), 'xyz',
                                      filename))
        for file_path in self.created_files:
            assert not os.path.exists(file_path), ("File already exists: " +
                                                   file_path)

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

        Check if the files already exist and raise an error if they do.
        """
        self.created_files = []
        filename = "test.xyz"
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

        for file_path in self.created_files:
            assert not os.path.exists(file_path), ("File already exists: " +
                                                   file_path)

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
