import unittest
import os
from lammpshade.Constructor import Simulation
from lammpshade.YAMLReader import YAMLReader
from lammpshade.GraphMaker import GraphMaker
from unittest.mock import patch


class Test_Simulation_init_(unittest.TestCase):
    """Tests the constructor of Simulation class"""

    def test_file_not_exists_Simulation(self):
        """GIVEN a file that does not exist
        WHEN creating a Simulation object with the file
        THEN it should raise a FileNotFoundError"""
        with self.assertRaises(FileNotFoundError):
            Simulation('test.yaml')
    
    def test_file_exists_Simulation(self):
        """GIVEN a file that exists
        WHEN creating a Simulation object with the file
        THEN it should create a Simulation object with the specified file path
        AND the thermo_keywords, thermo_data, and graphs attributes should be None"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        self.assertIsInstance(test.file, YAMLReader)
        self.assertIsNone(test.thermo_keywords)
        self.assertIsNone(test.thermo_data)


class Test_Simulation_convert_to_xyz(unittest.TestCase):
    """Tests the convert_to_xyz method of Simulation"""

    def test_convert_to_xyz_creates_file(self):
        """GIVEN a Simulation object and an output file path
        WHEN calling the convert_to_xyz method
        THEN it should create a file at the specified output file path
        AND the content of the file should be an empty string"""
        test = Simulation(os.path.join('tests', 'test_empty.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        self.assertEqual(test.output.filepath, output_path)
        with open(output_path, 'r') as f:
            self.assertEqual(f.read(), '')
        os.remove(output_path)

    def test_convert_to_xyz_writes_data(self):
        """GIVEN a Simulation object with thermo data and an output file path
        WHEN calling the convert_to_xyz method
        THEN it should create a file at the specified output file path
        AND the content of the file should match the expected data
        AND the thermo_keywords and thermo_data attributes of the Simulation object should match the expected data"""
        check_thermo_keywords = ['Step', 'Time', 'c_temp_up', 'c_temp_down', 'c_temp_glicerol', 'v_vcmy_glicerol', 'v_fcmx_diamup', 'v_fcmy_diamup', 'v_fcmz_diamup', 'v_fcmx_diamdown', 'v_fcmy_diamdown', 'v_fcmz_diamdown', 'v_fcmx_glicerol', 'v_fcmy_glicerol', 'v_fcmz_glicerol', 'v_vcmy_diamup', 'v_vcmy_diamdown']
        check_thermo_data = [[0, 0, 300.01337588855796, 301.4826602779623, 300.1499508622255, -2.8275435877824317e-06, -464.33419637917154, -263.0585406099187, -185.57297268783822, -77.10842905082524, 110.31226354857071, -140.2899523838907, 3.039668789182617, -5.06330135256117, 9.727313720915875, -3.1389946536884497e-05, -2.6631405961489187e-05],
                             [20, 1, 302.9835046598682, 301.87444362488395, 302.26813661366367, -2.8724272136338264e-06, -453.99482598635586, -326.24381431508033, -233.9726040510098, -42.210472839826075, 124.79690543736122, -122.74328293645766, 3.1868325247141094, -4.298221898942454, 9.276458616821385, -3.0941717500759274e-05, -2.9443466037842702e-05],
                             [40, 2, 302.8243689252428, 301.38668254523503, 304.22376702756196, -2.909264466469331e-06, -448.1659845051213, -386.817432548582, -269.80336944302906, -13.071858320137883, 128.84158150708203, -146.7292159255793, 3.121817604281661, -3.4342165171789922, 7.389085572389913, -2.97666226668858e-05, -3.2073229796614527e-05]
                             ]
        test = Simulation(os.path.join('tests', 'test.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        with open(output_path, 'r') as f:
            with open(os.path.join(os.getcwd(), 'tests', 'test_check.xyz'), 'r') as check:
                self.assertEqual(f.read(), check.read())
        self.assertEqual(test.thermo_keywords, check_thermo_keywords)
        for i, (data1, data2) in enumerate(zip(test.thermo_data, check_thermo_data)):
            for j, value1 in enumerate(data1):
                self.assertEqual(value1, data2[j])
        os.remove(output_path)

    def test_convert_to_xyz_no_thermo_data(self):
        """GIVEN a Simulation object without thermo data and an output file path
        WHEN calling the convert_to_xyz method
        THEN it should create a file at the specified output file path
        AND the thermo_keywords and thermo_data attributes of the Simulation object should be None"""
        test = Simulation(os.path.join('tests', 'test_nothermo.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        self.assertIsNone(test.thermo_keywords)
        self.assertIsNone(test.thermo_data)
        os.remove(output_path)

class Test_Simulation_get_thermodata(unittest.TestCase):
    """Tests the get_thermodata method of Simulation"""

    def test_get_thermodata(self):
        """GIVEN a Simulation object with thermo data
        WHEN calling the get_thermodata method
        THEN it should return the thermo data as a pandas DataFrame
        AND the thermo_keywords attribute of the Simulation object should match the expected data"""
        check_thermo_keywords = ['Step', 'Time', 'c_temp_up', 'c_temp_down', 'c_temp_glicerol', 'v_vcmy_glicerol', 'v_fcmx_diamup', 'v_fcmy_diamup', 'v_fcmz_diamup', 'v_fcmx_diamdown', 'v_fcmy_diamdown', 'v_fcmz_diamdown', 'v_fcmx_glicerol', 'v_fcmy_glicerol', 'v_fcmz_glicerol', 'v_vcmy_diamup', 'v_vcmy_diamdown']
        check_thermo_data = [[0, 0, 300.01337588855796, 301.4826602779623, 300.1499508622255, -2.8275435877824317e-06, -464.33419637917154, -263.0585406099187, -185.57297268783822, -77.10842905082524, 110.31226354857071, -140.2899523838907, 3.039668789182617, -5.06330135256117, 9.727313720915875, -3.1389946536884497e-05, -2.6631405961489187e-05],
                             [20, 1, 302.9835046598682, 301.87444362488395, 302.26813661366367, -2.8724272136338264e-06, -453.99482598635586, -326.24381431508033, -233.9726040510098, -42.210472839826075, 124.79690543736122, -122.74328293645766, 3.1868325247141094, -4.298221898942454, 9.276458616821385, -3.0941717500759274e-05, -2.9443466037842702e-05],
                             [40, 2, 302.8243689252428, 301.38668254523503, 304.22376702756196, -2.909264466469331e-06, -448.1659845051213, -386.817432548582, -269.80336944302906, -13.071858320137883, 128.84158150708203, -146.7292159255793, 3.121817604281661, -3.4342165171789922, 7.389085572389913, -2.97666226668858e-05, -3.2073229796614527e-05]
                             ]
        test = Simulation(os.path.join('tests', 'test.yaml'))
        thermo_data = test.get_thermodata()
        self.assertEqual(test.thermo_keywords, check_thermo_keywords)
        for i, (data1, data2) in enumerate(zip(thermo_data.values.tolist(), check_thermo_data)):
            for j, value1 in enumerate(data1):
                self.assertAlmostEqual(value1, data2[j], 10)

    def test_get_thermodata_empty_file(self):
        """GIVEN a Simulation object with an empty file
        WHEN calling the get_thermodata method
        THEN it should return None"""
        test = Simulation(os.path.join('tests', 'test_empty.yaml'))
        thermo_data = test.get_thermodata()
        self.assertIsNone(thermo_data)

    def test_get_thermodata_no_thermodata(self):
        """GIVEN a Simulation object without thermo data
        WHEN calling the get_thermodata method
        THEN it should return None"""
        test = Simulation(os.path.join('tests', 'test_nothermo.yaml'))
        thermo_data = test.get_thermodata()
        self.assertIsNone(thermo_data)

    def test_get_thermodata_file_already_read(self):
        """GIVEN a Simulation object with thermo data
        WHEN calling the get_thermodata method multiple times
        THEN it should return the same thermo data each time
        AND the thermo_keywords attribute of the Simulation object should match the expected data"""
        check_thermo_keywords = ['Step', 'Time', 'c_temp_up', 'c_temp_down', 'c_temp_glicerol', 'v_vcmy_glicerol', 'v_fcmx_diamup', 'v_fcmy_diamup', 'v_fcmz_diamup', 'v_fcmx_diamdown', 'v_fcmy_diamdown', 'v_fcmz_diamdown', 'v_fcmx_glicerol', 'v_fcmy_glicerol', 'v_fcmz_glicerol', 'v_vcmy_diamup', 'v_vcmy_diamdown']
        check_thermo_data = [[0, 0, 300.01337588855796, 301.4826602779623, 300.1499508622255, -2.8275435877824317e-06, -464.33419637917154, -263.0585406099187, -185.57297268783822, -77.10842905082524, 110.31226354857071, -140.2899523838907, 3.039668789182617, -5.06330135256117, 9.727313720915875, -3.1389946536884497e-05, -2.6631405961489187e-05],
                             [20, 1, 302.9835046598682, 301.87444362488395, 302.26813661366367, -2.8724272136338264e-06, -453.99482598635586, -326.24381431508033, -233.9726040510098, -42.210472839826075, 124.79690543736122, -122.74328293645766, 3.1868325247141094, -4.298221898942454, 9.276458616821385, -3.0941717500759274e-05, -2.9443466037842702e-05],
                             [40, 2, 302.8243689252428, 301.38668254523503, 304.22376702756196, -2.909264466469331e-06, -448.1659845051213, -386.817432548582, -269.80336944302906, -13.071858320137883, 128.84158150708203, -146.7292159255793, 3.121817604281661, -3.4342165171789922, 7.389085572389913, -2.97666226668858e-05, -3.2073229796614527e-05]
                             ]
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.get_thermodata()
        thermo_data = test.get_thermodata()
        self.assertEqual(test.thermo_keywords, check_thermo_keywords)
        for i, (data1, data2) in enumerate(zip(thermo_data.values.tolist(), check_thermo_data)):
            for j, value1 in enumerate(data1):
                self.assertAlmostEqual(value1, data2[j], 10)

class Test_Simulation_make_graphs(unittest.TestCase):
    """Tests the make_graphs method of Simulation"""

    @patch.object(GraphMaker, 'plot_graph')
    def test_make_graphs_display_mode(self, mock_plot_graph):
        """GIVEN a Simulation object
        WHEN calling the make_graphs method with mode='display'
        THEN it should create an instance of the GraphMaker class
        AND run the graphs in display mode"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='display')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_plot_graph.assert_called_once()

    @patch.object(GraphMaker, 'plot_graph')
    def test_make_graphs_display_mode_intial(self, mock_plot_graph):
        """GIVEN a Simulation object
        WHEN calling the make_graphs method with mode='d'
        THEN it should create an instance of the GraphMaker class
        AND run the graphs in display mode"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='d')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_plot_graph.assert_called_once()
    
    @patch.object(GraphMaker, 'plot_graph')
    def test_make_graphs_display_mode_spelling_error(self, mock_plot_graph):
        """GIVEN a Simulation object
        WHEN calling the make_graphs method with mode='dispay'
        THEN it should create an instance of the GraphMaker class
        AND run the graphs in display mode"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='dispay')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_plot_graph.assert_called_once()

    @patch.object(GraphMaker, 'interactive_mode')
    def test_make_graphs_interactive_mode(self, mock_interactive_mode):
        """GIVEN a Simulation object
        WHEN calling the make_graphs method with mode='interactive'
        THEN it should create an instance of the GraphMaker class
        AND run the graphs in interactive mode"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='interactive')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_interactive_mode.assert_called_once()
    
    @patch.object(GraphMaker, 'interactive_mode')
    def test_make_graphs_interactive_intial(self, mock_interactive_mode):
        """GIVEN a Simulation object
        WHEN calling the make_graphs method with mode='i'
        THEN it should create an instance of the GraphMaker class
        AND run the graphs in interactive mode"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='i')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_interactive_mode.assert_called_once()
    
    @patch.object(GraphMaker, 'interactive_mode')
    def test_make_graphs_interactive_spelling_error(self, mock_interactive_mode):
        """GIVEN a Simulation object
        WHEN calling the make_graphs method with mode='intactive'
        THEN it should create an instance of the GraphMaker class
        AND run the graphs in interactive mode"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='intactive')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_interactive_mode.assert_called_once()

    def test_make_graphs_ValueError(self):
        """GIVEN a Simulation object
        WHEN calling the make_graphs method with an invalid mode
        THEN it should raise a ValueError"""
        test = Simulation(os.path.join('tests', 'test.yaml'))
        with self.assertRaises(ValueError):
            test.make_graphs(mode='test')




if __name__ == '__main__':
    unittest.main()
