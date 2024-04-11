import unittest
import pandas as pd
from lammpshade.GraphMaker import GraphMaker
from unittest.mock import patch, MagicMock

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
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
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
    def test_plot_graph_with_df(self, mock_show, mock_subplots):
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

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.subplots', return_value=(MagicMock(), MagicMock()))
    def test_run_display_mode(self, mock_show, mock_subplots):
        """
        Test the run method with display mode.

        This test case checks if the run method correctly plots the graph when
        the mode is set to 'display'.

        The test passes if the graph is plotted without any errors.
        """
        keywords_list = ['mass', 'energy']
        self.graph_maker.run(keywords_list, mode='display')

    @patch('lammpshade.GraphMaker.GraphMaker.interactive_mode')
    def test_run_interactive_mode(self, mock_interactive_mode):
        """
        Test the run method with interactive mode.

        This test case checks if the run method correctly handles the interactive
        mode operations when the mode is set to 'interactive'.

        The test passes if the run method executes the interactive mode operations
        without any errors.
        """
        keywords_list = ['mass', 'energy']
        self.graph_maker.run(keywords_list, mode='interactive')
        self.assertTrue(mock_interactive_mode.called)

if __name__ == '__main__':
    unittest.main()
