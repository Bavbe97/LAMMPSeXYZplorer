import unittest
import os
from lammpshade.Constructor import Simulation
from lammpshade.YAMLReader import YAMLReader


class Test_Simulation_init(unittest.TestCase):
    """Tests the constructor of Simulation class"""

    def test_file_not_exists_Simulation(self):
        """Test the constructor of Simulation with a file that does not exist"""
        with self.assertRaises(FileNotFoundError):
            Simulation('test.yaml')
    
    def test_file_exists_Simulation(self):
        """Test the constructor of Simulation with a file that exists"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        self.assertIsInstance(test.file, YAMLReader)
        self.assertIsNone(test.thermo_keywords)
        self.assertIsNone(test.thermo_data)
        self.assertIsNone(test.graphs)


class Test_Simulation_convert_to_xyz(unittest.TestCase):
    """Tests the convert_to_xyz method of Simulation"""

    def test_convert_to_xyz_creates_file(self):
        """Test the convert_to_xyz method of Simulation"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        self.assertEqual(test.output.filepath, output_path)
        with open(output_path, 'r') as f:
            self.assertEqual(f.read(), '')

if __name__ == '__main__':
    unittest.main()
