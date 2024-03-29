import unittest
from unittest.mock import patch, MagicMock, mock_open
from lammpshade.XYZWriter import XYZWriter
import os
import tempfile

class Test_init_XYZWriter(unittest.TestCase):
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
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'xyz', filename)))
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))
    
    def test_file_already_exists(self):
        # Test if the file already exists and is opened
        filename = "existing_file.xyz"
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write("existing content")
        out = XYZWriter(filename)
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(out.output.writable()) 
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))
    
    def test_file_not_exists(self):
        # Test if the file is created if it does not exist
        filename = "new_file.xyz"
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(filename)
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(out.output.writable())
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))
    
    def test_create_file_in_different_filepath(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = "different_filepath.xyz"
            full_filepath = os.path.join(temp_dir, filename)
            out = XYZWriter(full_filepath)
            self.assertTrue(os.path.exists(full_filepath))
            self.assertTrue(out.output.writable()) 
            # Check if the file is created in the correct directory
            self.assertTrue(full_filepath.startswith(temp_dir))
            out.close_file()

class Test_write_to_xyz_XYZWriter(unittest.TestCase):

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

    def test_print_natoms(self):
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        data = {'natoms' : 10}
        with self.assertRaises(KeyError):
            out.write_to_xyz(data)
            with open(file_path, 'r') as file:
                content = file.read()
            self.assertIn(str(data['natoms']), content)
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))
    
    def test_no_natoms(self):
        filename = 'test.xyz'
        file_path = os.path.join(os.getcwd(), 'xyz', filename)
        out = XYZWriter(file_path)
        data = {'test' : 'fail'}
        with self.assertRaises(KeyError):
            out.write_to_xyz(data)
            self.assertTrue(os.path.exists(file_path))
        self.created_files.append(os.path.join(os.getcwd(), 'xyz', filename))


if __name__ == '__main__':
    unittest.main()