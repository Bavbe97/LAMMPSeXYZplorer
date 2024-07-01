import unittest
import os
from lammpshade.Constructor import Simulation
from lammpshade.YAMLReader import YAMLReader
from lammpshade.GraphMaker import GraphMaker
from unittest.mock import patch
import pandas as pd


class Test_Simulation_init_(unittest.TestCase):
    """
    Tests the constructor of Simulation class
    """
    def test_file_not_exists_Simulation(self):
        """
        Test if a Simulation object is created with a non-existing file.
        The expected behavior is that a FileNotFoundError is raised.

        Steps:
        1. Create a Simulation object with a non-existing file.
        2. Assert that a FileNotFoundError is raised.
        """
        with self.assertRaises(FileNotFoundError):
            Simulation('test.yaml')

    def test_file_exists_Simulation(self):
        """
        Test if a Simulation object is created with an existing file.
        The expected behavior is that the Simulation object is created
        successfully.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Assert that the `file` attribute of the Simulation object is an
           instance of YAMLReader.
        3. Assert that the `thermo_keywords` attribute of the Simulation object
           is None.
        4. Assert that the `thermo_data` attribute of the Simulation object is
           None.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        self.assertIsInstance(test.file, YAMLReader)
        self.assertIsNone(test.thermo_keywords)
        self.assertIsNone(test.thermo_data)


class Test_Simulation_convert_to_xyz(unittest.TestCase):
    """
    Test the convert_to_xyz method of Simulation class
    """
    def setUp(self):
        """
        Create a list of files that will be created during testing.
        The files will be created in the current working directory.

        Check if the files already exists and delete them if they do.
        Assert that the files do not exist.
        """
        self.created_files = []
        filename = "test.xyz"
        self.created_files.append(os.path.join(os.getcwd(), 'tests', filename))

        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        for file_path in self.created_files:
            assert not os.path.exists(file_path)

    def tearDown(self):
        """
        Remove the files created during testing.
        """
        # Clean up only the files created during testing
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_convert_to_xyz_creates_file(self):
        """
        Test if the convert_to_xyz method creates a file at the specified path.
        The expected behavior is that the output file is created.

        Steps:
        1. Create a Simulation object with an empty file.
        2. Call the convert_to_xyz method with the specified output path.
        3. Assert that the filepath attribute of the Simulation object is the
           same as the specified output path.
        4. Assert that the output file exists.
        """
        test = Simulation(os.path.join('tests', 'test_empty.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        self.assertEqual(test.output.filepath, output_path)
        self.assertTrue(os.path.exists(output_path))

    def test_convert_to_xyz_writes_data(self):
        """
        Test if the convert_to_xyz method writes the expected data to the
        output file.
        The expected behavior is that the output file contains the expected
        data.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the convert_to_xyz method with the specified output path.
        3. Open the output file and read the data.
        4. Open the check file and read the expected data.
        5. Assert that the data in the output file is the same as the expected
           data.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        with open(output_path, 'r') as f:
            with open(os.path.join(
                    os.getcwd(), 'tests', 'test_check.xyz'), 'r') as check:
                self.assertEqual(f.read(), check.read())

    def test_convert_to_xyz_no_thermo_data(self):
        """
        Test if the convert_to_xyz method works when no thermo data is present.
        The expected behavior is that the output file is created and the
        thermo_keywords and thermo_data attributes are None.

        Steps:
        1. Create a Simulation object with a file that does not contain thermo
           data.
        2. Call the convert_to_xyz method with the specified output path.
        3. Assert that the thermo_keywords attribute of the Simulation object
           is an empty list.
        4. Assert that the thermo_data attribute of the Simulation object is
           None.
        """

        test = Simulation(os.path.join('tests', 'test_nothermo.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        self.assertIsNone(test.thermo_keywords)
        self.assertIsNone(test.thermo_data)

    def test_convert_to_xyz_empty_file(self):
        """
        Test if the convert_to_xyz method works when the file is empty.
        The expected behavior is that an empty output file is created.

        Steps:
        1. Create a Simulation object with an empty file.
        2. Call the convert_to_xyz method with the specified output path.
        3. Assert that the output file is empty.
        """
        test = Simulation(os.path.join('tests', 'test_empty.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        test.convert_to_xyz(output_path)
        with open(output_path, 'r') as f:
            self.assertEqual(f.read(), '')

        """
        Test if no output path is specified.
        The expected behavior is that a TypeError is raised.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the convert_to_xyz method without specifying an output path.
        3. Assert that a TypeError is raised.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        with self.assertRaises(TypeError):
            test.convert_to_xyz()

    def test_convert_to_xyz_no_natoms(self):
        """
        Test if the number of atoms is not included in the input file.
        The expected behavior is that a KeyError is raised.
        """
        test = Simulation(os.path.join('tests', 'test_nonatoms.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        with self.assertRaises(KeyError):
            test.convert_to_xyz(output_path)

    def test_convert_to_xyz_no_atoms_keywords(self):
        """
        Test if required atom keywords are not included in the input file.
        The expected behavior is that a KeyError is raised.
        """
        test = Simulation(os.path.join('tests', 'test_noatomskeywords.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        with self.assertRaises(KeyError):
            test.convert_to_xyz(output_path)

    def test_convert_to_xyz_no_atoms_data(self):
        """
        Test if atom data is not included in the input file.
        The expected behavior is that a KeyError is raised.
        """
        test = Simulation(os.path.join('tests', 'test_noatomsdata.yaml'))
        output_path = os.path.join(os.getcwd(), 'tests', 'test.xyz')
        with self.assertRaises(KeyError):
            test.convert_to_xyz(output_path)


class Test_Simulation_get_thermodata(unittest.TestCase):
    """
    Test the get_thermodata method of Simulation
    """

    def test_get_thermodata(self):
        """
        Test if the get_thermodata method returns the expected thermo data.
        The expected behavior is that the method returns the expected thermo
        data as a pandas DataFrame and the thermo_keywords and thermo_data
        attributes are set.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the get_thermodata method.
        3. Assert that the thermo_keywords attribute of the Simulation object
           matches the expected data.
        4. Assert that the thermo_data attribute of the Simulation object
           matches the expected data.
        5. Assert that the returned thermo_data is a pandas DataFrame.
        6. Assert that the returned thermo_data pandas DataFrame is the same as
           the expected data.
        """
        check_thermo_keywords = [
            'Step', 'Time', 'c_temp_up', 'c_temp_down', 'c_temp_glicerol',
            'v_vcmy_glicerol', 'v_fcmx_diamup', 'v_fcmy_diamup',
            'v_fcmz_diamup', 'v_fcmx_diamdown', 'v_fcmy_diamdown',
            'v_fcmz_diamdown', 'v_fcmx_glicerol', 'v_fcmy_glicerol',
            'v_fcmz_glicerol', 'v_vcmy_diamup', 'v_vcmy_diamdown'
        ]
        check_thermo_data = [
            [0, 0, 300.01337588855796, 301.4826602779623, 300.1499508622255,
             -2.8275435877824317e-06, -464.33419637917154, -263.0585406099187,
             -185.57297268783822, -77.10842905082524, 110.31226354857071,
             -140.2899523838907, 3.039668789182617, -5.06330135256117,
             9.727313720915875, -3.1389946536884497e-05,
             -2.6631405961489187e-05],
            [20, 1, 302.9835046598682, 301.87444362488395, 302.26813661366367,
             -2.8724272136338264e-06, -453.99482598635586, -326.24381431508033,
             -233.9726040510098, -42.210472839826075, 124.79690543736122,
             -122.74328293645766, 3.1868325247141094, -4.298221898942454,
             9.276458616821385, -3.0941717500759274e-05,
             -2.9443466037842702e-05],
            [40, 2, 302.8243689252428, 301.38668254523503, 304.22376702756196,
             -2.909264466469331e-06, -448.1659845051213, -386.817432548582,
             -269.80336944302906, -13.071858320137883, 128.84158150708203,
             -146.7292159255793, 3.121817604281661, -3.4342165171789922,
             7.389085572389913, -2.97666226668858e-05,
             -3.2073229796614527e-05]
        ]

        check_thermo_data_df = pd.DataFrame(check_thermo_data,
                                            columns=check_thermo_keywords)

        test = Simulation(os.path.join('tests', 'test.yaml'))
        thermo_data = test.get_thermodata()
        self.assertEqual(test.thermo_keywords, check_thermo_keywords)
        self.assertTrue(test.thermo_data == check_thermo_data)

        self.assertIsInstance(thermo_data, pd.DataFrame)
        self.assertTrue(thermo_data.equals(check_thermo_data_df))

    def test_get_thermodata_empty_file(self):
        """
        Test if the get_thermodata method returns None when the file is empty.

        Steps:
        1. Create a Simulation object with an empty file.
        2. Call the get_thermodata method.
        3. Assert that the returned thermo_data is None.
        """
        test = Simulation(os.path.join('tests', 'test_empty.yaml'))
        thermo_data = test.get_thermodata()
        self.assertIsNone(thermo_data)

    def test_get_thermodata_no_thermo_data(self):
        """
        Test if the get_thermodata method returns None when no thermo data is
        present.

        Steps:
        1. Create a Simulation object with a file that does not contain thermo
           data.
        2. Call the get_thermodata method.
        3. Assert that the returned thermo_data is None.
        """
        test = Simulation(os.path.join('tests', 'test_nothermo.yaml'))

        self.assertIsNone(test.get_thermodata())

    def test_get_thermodata_file_already_read(self):
        """
        Test if the get_thermodata method returns the same thermo data when
        called multiple times.
        The expected behavior is that the method returns the same thermo data
        pandas DataFrame each time it is called.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the get_thermodata method multiple times.
        3. Assert that the returned thermo data pandas DataFrame is the same
           each time.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))

        thermo_data_1 = test.get_thermodata()
        thermo_data_2 = test.get_thermodata()
        thermo_data_3 = test.get_thermodata()

        self.assertTrue(thermo_data_1.equals(thermo_data_2))
        self.assertTrue(thermo_data_2.equals(thermo_data_3))


class Test_Simulation_get_step_thermodata(unittest.TestCase):
    """
    Test the get_step_thermodata method of Simulation
    """
    def test_get_step_thermodata(self):
        """
        Test if the get_step_thermodata method returns the expected thermo data
        for a given step.
        The expected behavior is that the method returns the expected thermo
        data for the specified step and returns True.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Create a step dictionary with thermo data.
        3. Call the get_step_thermodata method with the step dictionary.
        4. Assert that the thermo_data attribute of the Simulation object is
           the same as the expected data.
        5. Assert that the method returns True.
        """
        step = {'thermo': {'keywords': ['Step', 'Time', 'c_temp', 'v_vel',
                                        'v_force', 'test'],
                           'data': [0, 1, 6, -11.3, 999, 'test']}}
        check_thermo_data = [[0, 1, 6, -11.3, 999, 'test']]

        test = Simulation(os.path.join('tests', 'test.yaml'))
        thermo_flag = test.get_step_thermodata(step)
        thermo_data = test.thermo_data
        self.assertTrue(thermo_data == check_thermo_data)
        self.assertTrue(thermo_flag)

    def test_get_step_thermodata_no_thermo_data(self):
        """
        Test if the get_step_thermodata method returns False when no thermo
        data is present in the step dictionary.
        The expected behavior is that the method returns False.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Create a step dictionary without thermo data.
        3. Call the get_step_thermodata method with the step dictionary.
        4. Assert that the method returns False.
        """
        step = {'thermo': {'keywords': ['Step', 'Time', 'c_temp', 'v_vel',
                                        'v_force', 'test'],
                           'data': []}}

        test = Simulation(os.path.join('tests', 'test.yaml'))
        thermo_flag = test.get_step_thermodata(step)
        self.assertFalse(thermo_flag)

    def test_get_step_thermodata_no_thermo_keywords(self):
        """
        Test if the get_step_thermodata method returns False when no thermo
        keywords are present in the step dictionary.
        The expected behavior is that the method returns False.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Create a step dictionary without thermo keywords.
        3. Call the get_step_thermodata method with the step dictionary.
        4. Assert that the method returns False.
        """
        step = {'thermo': {'data': [0, 1, 6, -11.3, 999, 'test']}}

        test = Simulation(os.path.join('tests', 'test.yaml'))
        thermo_flag = test.get_step_thermodata(step)
        self.assertFalse(thermo_flag)


class Test_Simulation_check_thermo_data(unittest.TestCase):
    """
    Test the check_thermo_data method of Simulation
    """
    def test_check_thermo_data(self):
        """
        Test if the thermo data is present in the Simulation object.
        The expected behavior is that the method returns True.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the check_thermo_data method.
        3. Assert that the method returns True.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        step = test.file.get_next_step()
        self.assertTrue(test.check_thermo_data(step))

    def test_check_thermo_data_no_thermo_data(self):
        """
        Test if the thermo data is not present in the Simulation object.
        The expected behavior is that the method returns False.

        Steps:
        1. Create a Simulation object with a file that does not contain thermo
           data.
        2. Call the check_thermo_data method.
        3. Assert that the method returns False.
        """
        test = Simulation(os.path.join('tests', 'test_nothermo.yaml'))
        step = test.file.get_next_step()
        self.assertFalse(test.check_thermo_data(step))

    def test_check_thermo_data_empty_file(self):
        """
        Test if the file is empty.
        The expected behavior is that the method returns False.

        Steps:
        1. Create a Simulation object with an empty file.
        2. Call the check_thermo_data method.
        3. Assert that the method returns False.
        """
        test = Simulation(os.path.join('tests', 'test_empty.yaml'))
        step = test.file.get_next_step()
        self.assertFalse(test.check_thermo_data(step))


class Test_Simulation_make_graphs(unittest.TestCase):
    """
    Test the make_graphs method of Simulation
    """

    @patch.object(GraphMaker, 'plot_graph')
    def test_make_graphs_display_mode(self, mock_plot_graph):
        """
        Test if the make_graphs method creates a GraphMaker object and runs the
        graphs in display mode.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the make_graphs method with mode='display'.
        3. Assert that the graphs attribute of the Simulation object is an
           instance of GraphMaker.
        4. Assert that the plot_graph method of the GraphMaker object is called
           once.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='display')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_plot_graph.assert_called_once()

    @patch.object(GraphMaker, 'plot_graph')
    def test_make_graphs_display_mode_intial(self, mock_plot_graph):
        """
        Test if the make_graphs method creates a GraphMaker object and runs the
        graphs in display mode when mode='d'.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the make_graphs method with mode='d'.
        3. Assert that the graphs attribute of the Simulation object is an
           instance of GraphMaker.
        4. Assert that the plot_graph method of the GraphMaker object is called
           once.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='d')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_plot_graph.assert_called_once()

    @patch.object(GraphMaker, 'plot_graph')
    def test_make_graphs_display_mode_spelling_error(self, mock_plot_graph):
        """
        Test if the make_graphs method creates a GraphMaker object and runs the
        graphs in display mode when mode='dispay'.
        The expected behavior is that the method runs the graphs in display
        mode.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the make_graphs method with mode='dispay'.
        3. Assert that the graphs attribute of the Simulation object is an
           instance of GraphMaker.
        4. Assert that the plot_graph method of the GraphMaker object is called
           once.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='dispay')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_plot_graph.assert_called_once()

    @patch.object(GraphMaker, 'interactive_mode')
    def test_make_graphs_interactive_mode(self, mock_interactive_mode):
        """
        Test if the make_graphs method creates a GraphMaker object and runs the
        graphs in interactive mode.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the make_graphs method with mode='interactive'.
        3. Assert that the graphs attribute of the Simulation object is an
           instance of GraphMaker.
        4. Assert that the interactive_mode method of the GraphMaker object is
           called once.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='interactive')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_interactive_mode.assert_called_once()

    @patch.object(GraphMaker, 'interactive_mode')
    def test_make_graphs_interactive_intial(self, mock_interactive_mode):
        """
        Test if the make_graphs method creates a GraphMaker object and runs the
        graphs in interactive mode when mode='i'.
        The expected behavior is that the method runs the graphs in interactive
        mode.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the make_graphs method with mode='i'.
        3. Assert that the graphs attribute of the Simulation object is an
           instance of GraphMaker.
        4. Assert that the interactive_mode method of the GraphMaker object is
           called once.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='i')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_interactive_mode.assert_called_once()

    @patch.object(GraphMaker, 'interactive_mode')
    def test_make_graphs_interactive_spelling_error(
        self, mock_interactive_mode
    ):
        """
        Test if the make_graphs method creates a GraphMaker object and runs the
        graphs in interactive mode when mode='intactive'.
        The expected behavior is that the method runs the graphs in interactive
        mode.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the make_graphs method with mode='intactive'.
        3. Assert that the graphs attribute of the Simulation object is an
           instance of GraphMaker.
        4. Assert that the interactive_mode method of the GraphMaker object is
           called once.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        test.make_graphs(mode='intactive')
        self.assertIsInstance(test.graphs, GraphMaker)
        mock_interactive_mode.assert_called_once()

    def test_make_graphs_ValueError(self):
        """
        Test if the make_graphs method raises a ValueError when an invalid mode
        is provided.

        Steps:
        1. Create a Simulation object with the specified file path.
        2. Call the make_graphs method with an invalid mode.
        3. Assert that a ValueError is raised.
        """
        test = Simulation(os.path.join('tests', 'test.yaml'))
        with self.assertRaises(ValueError):
            test.make_graphs(mode='test')


if __name__ == '__main__':
    unittest.main()
