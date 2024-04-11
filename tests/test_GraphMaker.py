import sys
import unittest
import pandas as pd
from lammpshade.GraphMaker import GraphMaker
from unittest.mock import patch, MagicMock
from io import StringIO

class Test_GraphMaker_init_(unittest.TestCase):
    """
    Test case for the initialization of the GraphMaker class.
    """

    def test_init(self):
        """
        Test the initialization of the GraphMaker class.

        This test case checks if the GraphMaker class is initialized correctly by comparing the
        df attribute of the created GraphMaker instance with a test DataFrame.

        The test DataFrame is created using the data and keywords lists. The
        data list contains sample data, and the keywords list contains the column
        names for the DataFrame.

        The test passes if the df attribute of the GraphMaker instance is equal to the
        test DataFrame.

        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df)
        self.assertEqual(graph_maker.df.values.tolist(), test_df.values.tolist())
        self.assertEqual(graph_maker.df.columns.tolist(), test_df.columns.tolist())
    
    def test_init_empty_df(self):
        """
        Test the initialization of the GraphMaker class with empty DataFrame.

        This test case checks if the GraphMaker class raises a ValueError when
        initialized with empty DataFrame.

        The test passes if the GraphMaker class raises a ValueError when initialized
        with empty DataFrame.

        """
        data = []
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        with self.assertRaises(ValueError):
            GraphMaker(test_df)
    
    def test_init_with_keywords_list(self):
        """
        Test the initialization of the GraphMaker class with a keywords list.

        This test case checks if the GraphMaker class is initialized correctly when
        a keywords list is provided. It compares the keywords_list attribute of the
        created GraphMaker instance with the provided keywords list.

        The test passes if the keywords_list attribute of the GraphMaker instance is
        equal to the provided keywords list.

        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        test_keywords_list = ['mass', 'distance', 'vel']
        graph_maker = GraphMaker(test_df, keywords_list=test_keywords_list)
        self.assertEqual(graph_maker.keywords_list, test_keywords_list)

class Test_GraphMaker_process_columns(unittest.TestCase):
    """
    Test case for the process_columns method of the GraphMaker class.
    """

    def test_process_columns_with_keywords(self):
        """
        Test the process_columns method with provided keywords.

        This test case checks if the process_columns method returns the expected list
        of matching column names when provided with a list of keywords.

        The test passes if the returned list of matching column names is equal to the
        expected list of matching column names.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df, keywords_list=['mass', 'energy', 'velocity'])
        expected_columns = ['mass', 'energy', 'velocity']
        self.assertEqual(graph_maker.process_columns(), expected_columns)

    def test_process_columns_without_keywords(self):
        """
        Test the process_columns method without provided keywords.

        This test case checks if the process_columns method returns all the column names
        when no keywords are provided.

        The test passes if the returned list of column names is equal to the list of all
        column names in the DataFrame.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df)
        expected_columns = keywords
        self.assertListEqual(graph_maker.process_columns(), expected_columns)

    def test_process_columns_no_matches(self):
        """
        Test the process_columns method with no matching columns.

        This test case checks if the process_columns method returns an empty list when
        no columns match the provided keywords.

        The test passes if the returned list of matching column names is empty.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df, keywords_list=['force', 'pressure', 'temperature'])
        expected_columns = []
        self.assertListEqual(graph_maker.process_columns(), expected_columns)

    def test_process_columns_partially_matches(self):
        """
        Test the process_columns method with partial matches.

        This test case checks if the process_columns method returns the list of
        column names that partially match the provided keywords.

        The test passes if the returned list of matching column names contains
        the columns that partially match the provided keywords.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df, keywords_list=['mass', 'force', 'velocity'])
        expected_columns = ['mass', 'velocity']
        self.assertListEqual(graph_maker.process_columns(), expected_columns)

class Test_GraphMaker_plot_graph(unittest.TestCase):
    """
    Test case for the plot_graph method of the GraphMaker class.
    """

    def setUp(self):
        """
        Set up test data and objects.
        """
        data = [[1, 2, 3, 4 , 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15]]
        keywords = ['mass', 'distance', 'Time', 'energy', 'velocity']
        self.test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(self.test_df)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.subplots', return_value=(MagicMock(), MagicMock()))
    def test_plot_graph_with_columns(self, mock_subplots, mock_show):
        """
        Test the plot_graph method with provided columns.

        This test case checks if the plot_graph method plots the graph correctly
        when provided with a list of columns.

        The test passes if the graph is plotted without any errors.
        """
        # Create a mock for the ax object
        mock_fig, mock_ax = mock_subplots.return_value

        columns = ['mass', 'energy']
        self.graph_maker.plot_graph(columns)

        # Verify that ax.plot was called the correct number of times
        self.assertEqual(mock_ax.plot.call_count, len(columns))

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.subplots', return_value=(MagicMock(), MagicMock()))
    def test_plot_graph_with_df(self, mock_subplots, mock_show):
        """
        Test the plot_graph method with provided dataframe.

        This test case checks if the plot_graph method plots the graph correctly
        when provided with a dataframe.

        The test passes if the graph is plotted without any errors.
        """
        # Create a mock for the ax object
        mock_fig, mock_ax = mock_subplots.return_value

        columns = ['mass', 'energy']
        self.graph_maker.plot_graph(columns, df=self.test_df)

        # Verify that ax.plot was called the correct number of times
        self.assertEqual(mock_ax.plot.call_count, len(columns))

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.subplots')
    def test_plot_graph_with_x_y(self, mock_subplots, mock_show):
        """
        Test the plot_graph method with provided x and y values.

        This test case checks if the plot_graph method plots the graph correctly
        when provided with x and y values.

        The test passes if the graph is plotted without any errors.
        """
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        # Create a mock for the ax object
        mock_ax = MagicMock()
        mock_subplots.return_value = (MagicMock(), mock_ax)

        self.graph_maker.plot_graph([], x=x, y=y)

        # Verify that ax.plot was called with the expected arguments
        mock_ax.plot.assert_called_once_with(x, y)

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.subplots', return_value=(MagicMock(), MagicMock()))
    def test_plot_graph_default(self, mock_subplots, mock_show):
        """
        Test the plot_graph method with default parameters.

        This test case checks if the plot_graph method plots the graph correctly
        with default parameters.

        The test passes if the graph is plotted without any errors.
        """
        # Create a mock for the ax object
        mock_fig, mock_ax = mock_subplots.return_value

        self.graph_maker.plot_graph([])

        # Verify that ax.plot was called the correct number of times
        self.assertEqual(mock_ax.plot.call_count, len(self.test_df.columns) - 1)
    
class Test_GraphMaker_run(unittest.TestCase):
    """
    Test case for the run method of the GraphMaker class.
    """

    def setUp(self):
        """
        Set up test data and objects.
        """
        data = [[1, 2, 3, 4 , 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        self.test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(self.test_df)

    def test_run_default_mode(self):
        """
        Test the run method with default mode.

        This test case checks if the run method correctly calls the plot_graph method
        with the processed columns when the default mode is specified.

        The test passes if the plot_graph method is called with the correct arguments.
        """
        columns = ['mass', 'distance', 'time', 'energy', 'velocity']
        with patch.object(self.graph_maker, 'process_columns', return_value=columns) as mock_process_columns:
            with patch.object(self.graph_maker, 'plot_graph') as mock_plot_graph:
                self.graph_maker.run('default')
                mock_process_columns.assert_called_once()
                mock_plot_graph.assert_called_once_with(columns)

        with patch.object(self.graph_maker, 'process_columns', return_value=columns) as mock_process_columns:
            with patch.object(self.graph_maker, 'plot_graph') as mock_plot_graph:
                self.graph_maker.run('def')
                mock_process_columns.assert_called_once()
                mock_plot_graph.assert_called_once_with(columns)
        
        with patch.object(self.graph_maker, 'process_columns', return_value=columns) as mock_process_columns:
            with patch.object(self.graph_maker, 'plot_graph') as mock_plot_graph:
                self.graph_maker.run('d')
                mock_process_columns.assert_called_once()
                mock_plot_graph.assert_called_once_with(columns)

        with patch.object(self.graph_maker, 'process_columns', return_value=columns) as mock_process_columns:
            with patch.object(self.graph_maker, 'plot_graph') as mock_plot_graph:
                self.graph_maker.run('deflt')
                mock_process_columns.assert_called_once()
                mock_plot_graph.assert_called_once_with(columns)

    def test_run_interactive_mode(self):
        """
        Test the run method with interactive mode.

        This test case checks if the run method correctly calls the interactive_mode method
        when the interactive mode is specified.

        The test passes if the interactive_mode method is called.
        """
        with patch.object(self.graph_maker, 'interactive_mode') as mock_interactive_mode:
            self.graph_maker.run('interactive')
            mock_interactive_mode.assert_called_once()
            
        with patch.object(self.graph_maker, 'interactive_mode') as mock_interactive_mode:
            self.graph_maker.run('int')
            mock_interactive_mode.assert_called_once()

        with patch.object(self.graph_maker, 'interactive_mode') as mock_interactive_mode:
            self.graph_maker.run('i')
            mock_interactive_mode.assert_called_once()

        with patch.object(self.graph_maker, 'interactive_mode') as mock_interactive_mode:
            self.graph_maker.run('inteactive')
            mock_interactive_mode.assert_called_once()

    def test_run_invalid_mode(self):
        """
        Test the run method with invalid mode.

        This test case checks if the run method raises a ValueError when an invalid mode is specified.

        The test passes if a ValueError is raised.
        """
        with self.assertRaises(ValueError):
            self.graph_maker.run('test')

class Test_GraphMaker_interactive_mode(unittest.TestCase):
    """
    Test case for the interactive_mode method of the GraphMaker class.
    """

    @patch('builtins.input', side_effect=['mass', 'exit'])
    @patch('builtins.print')
    def test_interactive_mode_exit(self, mock_print, mock_input):
        """
        Test the interactive_mode method when the user types "exit".

        This test case checks if the interactive_mode method exits the program
        when the user types "exit".

        The test passes if the program exits without any errors.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df)

        graph_maker.interactive_mode()

        mock_print.assert_called_with("""Combine - Displays a single figure with all "Time vs. Quantity" data plotted together.""")
        mock_input.assert_called_with('Select which quantities to display and how: ')

    @patch('builtins.input', side_effect=['Display [mass, energy]', 'exit'])
    @patch('builtins.print')
    @patch.object(GraphMaker, 'plot_graph')
    def test_interactive_mode_display_mode(self, mock_plot_graph, mock_print, mock_input):
        """
        Test the interactive_mode method with Display mode.

        This test case checks if the interactive_mode method calls the plot_graph
        method with the correct arguments when the user selects Display mode.

        The test passes if the plot_graph method is called with the correct arguments.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df)

        graph_maker.interactive_mode()

        mock_print.assert_called_with('Combine - Displays a single figure with all "Time vs. Quantity" data plotted together.')
        mock_input.assert_called_with('Select which quantities to display and how: ')
        mock_plot_graph.assert_called_with(['energy'])

    @patch('builtins.input', side_effect=['Combine [mass, energy]', 'exit'])
    @patch('builtins.print')
    @patch.object(GraphMaker, 'plot_graph')
    def test_interactive_mode_combine_mode(self, mock_plot_graph, mock_print, mock_input):
        """
        Test the interactive_mode method with Combine mode.

        This test case checks if the interactive_mode method calls the plot_graph
        method with the correct arguments when the user selects Combine mode.

        The test passes if the plot_graph method is called with the correct arguments.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df)

        graph_maker.interactive_mode()

        mock_print.assert_called_with('Combine - Displays a single figure with all "Time vs. Quantity" data plotted together.')
        mock_input.assert_called_with('Select which quantities to display and how: ')
        mock_plot_graph.assert_called_with(['mass', 'energy'])

if __name__ == '__main__':
    unittest.main()
