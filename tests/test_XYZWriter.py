import unittest
from lammpshade.XYZWriter import XYZWriter
import os
import tempfile


class Test_XYZWriter_init_(unittest.TestCase):
    def setUp(self):
        self.created_files = []

    def tearDown(self):
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_file_endswith_xyz(self):
        # Test if the file ends with '.xyz'
        with self.assertRaises(ValueError):
            XYZWriter("example.txt")

    def test_file_created_in_output_directory(self):
        # Test if the file is created in the "./xyz/" directory
        filename = "test_output.xyz"
        output = XYZWriter(filename)
        with output as out:
            self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'xyz',
                                                        filename)))
            self.assertTrue(out.output.writable())
            self.created_files.append(os.path.join(os.getcwd(), 'xyz',
                                                   filename))

    def test_file_already_exists(self):
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
            self.created_files.append(os.path.join(os.getcwd(), 'xyz',
                                                   filename))

    def test_file_not_exists(self):
        # Test if the file is created if it does not exist
        filename = "new_file.xyz"
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        output = XYZWriter(filename)
        with output:
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(output.output.writable())
            self.created_files.append(os.path.join(os.getcwd(), 'xyz',
                                                   filename))

    def test_create_file_in_different_filepath(self):
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

    def setUp(self):
        self.created_files = []

    def tearDown(self):
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_write_to_xyz(self):
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
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

    def test_no_data(self):
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        step = {'natoms': 10, 'keywords': ['id', 'type', 'mass', 'element',
                                           'x', 'y', 'z', 'vx', 'vy', 'vz',
                                           'fx', 'fy', 'fz']}
        with self.assertRaises(KeyError):
            out.write_to_xyz(step)
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

    def test_no_atoms(self):
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        data = {'natoms': 10}
        with self.assertRaises(KeyError):
            out.write_to_xyz(data)

    def test_no_element_coordinates(self):
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
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

    def test_thermo_data_no_box(self):
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
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))

    def test_thermo_data_yes_box(self):
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
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))


class Test_XYZWriter_contest_manager(unittest.TestCase):
    def setUp(self):
        self.created_files = []

    def tearDown(self):
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Remove the 'output' directory if it's empty
        output_dir = os.path.join(os.getcwd(), 'xyz')
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            os.rmdir(output_dir)

    def test_enter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = 'test.xyz'
            file_path = os.path.join(temp_dir, filename)
            output = XYZWriter(file_path)
            with output as out:
                self.assertTrue(os.path.exists(file_path))
                self.assertTrue(out.output.writable())
                self.created_files.append(file_path)

    def test_exit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = 'test.xyz'
            file_path = os.path.join(temp_dir, filename)
            output = XYZWriter(file_path)
            with output:
                pass
        self.assertFalse(os.path.exists(file_path))
        self.created_files.append(file_path)


if __name__ == '__main__':
    unittest.main()
