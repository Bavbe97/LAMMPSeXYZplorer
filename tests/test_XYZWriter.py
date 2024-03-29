import unittest
from unittest.mock import patch, MagicMock, mock_open
from lammpshade.XYZWriter import XYZWriter
import os
import tempfile

class TestXYZWriter(unittest.TestCase):
    def setUp(self):
        self.created_files = []

    def tearDown(self):
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

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


if __name__ == '__main__':
    unittest.main()