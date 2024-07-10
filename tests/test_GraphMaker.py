import unittest
import pandas as pd
from lammpshade.GraphMaker import GraphMaker
from unittest.mock import patch, MagicMock, call


class Test_GraphMaker_init_(unittest.TestCase):
    """
    Test case for the initialization of the GraphMaker class.
    """

    def test_init(self):
        """
        Test if the GraphMaker class is initialized correctly.
        The expected behavior is that the GraphMaker class is initialized
        correctly when provided with a non-empty DataFrame.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Assert that the df attribute of the GraphMaker instance is equal to
           the test DataFrame.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df)
        self.assertEqual(graph_maker.df.values.tolist(),
                         test_df.values.tolist())
        self.assertEqual(graph_maker.df.columns.tolist(),
                         test_df.columns.tolist())

    def test_init_empty_df(self):
        """
        Test if the GraphMaker class raises a ValueError with an empty
        DataFrame.

        Steps:
        1. Create an empty DataFrame.
        2. Attempt to create an instance of the GraphMaker class with the empty
           DataFrame.
        3. Assert that a ValueError is raised.
        """
        data = []
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        with self.assertRaises(ValueError):
            GraphMaker(test_df)

    def test_init_with_keywords_list(self):
        """
        Test if the GraphMaker class is initialized correctly with a keywords
        list.
        The expected behavior is that the GraphMaker class is initialized
        correctly when provided with a non-empty DataFrame and a keywords list.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame
           and a keywords list.
        3. Assert that the keywords_list attribute of the GraphMaker instance
           is equal to the provided keywords list.
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
        Test if the process_columns method returns the correct list of matching
        columns when provided with a list of keywords.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame
           and a list of keywords.
        3. Call the process_columns method of the GraphMaker instance.
        4. Assert that the returned list of matching column names is equal to
           the expected list of matching column names.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(
            test_df, keywords_list=['mass', 'energy', 'velocity']
        )
        expected_columns = ['mass', 'energy', 'velocity']
        self.assertEqual(graph_maker.process_columns(), expected_columns)

    def test_process_columns_without_keywords(self):
        """
        Test if the process_columns method returns all the column names when no
        keywords are provided.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Call the process_columns method of the GraphMaker instance.
        4. Assert that the returned list of column names is equal to the list
           of all column names in the DataFrame.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(test_df)
        expected_columns = keywords
        self.assertListEqual(graph_maker.process_columns(), expected_columns)

    def test_process_columns_no_matches(self):
        """
        Test if the process_columns method returns an empty list when no
        columns match the provided keywords.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame
           and a list of keywords that do not match any column names.
        3. Call the process_columns method of the GraphMaker instance.
        4. Assert that the returned list of matching column names is empty.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(
            test_df,
            keywords_list=['force', 'pressure', 'temperature']
        )
        expected_columns = []
        self.assertListEqual(graph_maker.process_columns(), expected_columns)

    def test_process_columns_partially_matches(self):
        """
        Test if the process_columns method returns the correct list of matching
        columns when provided with keywords that partially match the column
        names.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame
           and a list of keywords that partially match the column names.
        3. Call the process_columns method of the GraphMaker instance.
        4. Assert that the returned list of matching column names is equal to
           the expected list of matching column names.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        graph_maker = GraphMaker(
            test_df,
            keywords_list=['mass', 'force', 'velocity']
        )
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
        data = [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15]]
        keywords = ['mass', 'distance', 'Time', 'energy', 'velocity']
        self.test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(self.test_df)

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.subplots',
           return_value=(MagicMock(), MagicMock()))
    def test_plot_graph_with_columns(self, mock_subplots, mock_show):
        """
        Test if the plot_graph method plots the graph correctly when provided
        with column names.

        Steps:
        1. Create a mock for the subplots function.
        2. Call the plot_graph method of the GraphMaker instance with a list of
           column names.
        3. Assert that the ax.plot method was called the correct number of
           times.
        4. Assert that the ax.plot method was called with the expected
           arguments.
        5. Assert that the show method was called once.
        """
        # Create a mock for the ax object
        mock_fig, mock_ax = mock_subplots.return_value

        columns = ['mass', 'energy']
        self.graph_maker.plot_graph(columns)

        # Verify that ax.plot was called the correct number of times
        self.assertEqual(mock_ax.plot.call_count, len(columns))

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.subplots',
           return_value=(MagicMock(), MagicMock()))
    def test_plot_graph_with_df(self, mock_subplots, mock_show):
        """
        Test if the plot_graph method plots the graph correctly when provided
        with a DataFrame.

        Steps:
        1. Create a mock for the subplots function.
        2. Call the plot_graph method of the GraphMaker instance with a
           DataFrame.
        3. Assert that the ax.plot method was called the correct number of
           times.
        4. Assert that the ax.plot method was called with the expected
           arguments.
        5. Assert that the show method was called once.
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
        Test if the plot_graph method plots the graph correctly when provided
        with x and y values.

        Steps:
        1. Create a mock for the subplots function.
        2. Call the plot_graph method of the GraphMaker instance with x and y
           values.
        3. Assert that the ax.plot method was called once.
        4. Assert that the ax.plot method was called with the expected
           arguments.
        5. Assert that the show method was called once.
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
    @patch('matplotlib.pyplot.subplots',
           return_value=(MagicMock(), MagicMock()))
    def test_plot_graph_default(self, mock_subplots, mock_show):
        """
        Test if the plot_graph method plots the graph correctly with default
        arguments.

        Steps:
        1. Create a mock for the subplots function.
        2. Call the plot_graph method of the GraphMaker instance with default
           arguments.
        3. Assert that the ax.plot method was called the correct number of
           times.
        4. Assert that the show method was called once.
        """
        # Create a mock for the ax object
        mock_fig, mock_ax = mock_subplots.return_value

        self.graph_maker.plot_graph([])

        # Verify that ax.plot was called the correct number of times
        expected_call_count = len(self.test_df.columns) - 1
        self.assertEqual(mock_ax.plot.call_count, expected_call_count)


class Test_GraphMaker_run(unittest.TestCase):
    """
    Test case for the run method of the GraphMaker class.
    """

    def setUp(self):
        """
        Set up test data and objects.
        """
        data = [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        self.test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(self.test_df)

    def test_run_default_mode(self):
        """
        Test if the run method correctly calls the process_columns and
        plot_graph methods with the correct arguments when the default mode is
        specified.

        Steps:
        1. Create a mock for the process_columns method.
        2. Create a mock for the plot_graph method.
        3. Call the run method of the GraphMaker instance with the default
           mode.
        4. Assert that the process_columns method was called once.
        5. Assert that the plot_graph method was called once with the correct
           arguments.
        """
        columns = ['mass', 'distance', 'time', 'energy', 'velocity']
        with patch.object(self.graph_maker, 'process_columns',
                          return_value=columns) as mock_process_columns, (
                patch.object(self.graph_maker, 'plot_graph')
                ) as mock_plot_graph:
            self.graph_maker.run('default')
            mock_process_columns.assert_called_once()
            mock_plot_graph.assert_called_once_with(columns)

        with patch.object(self.graph_maker, 'process_columns',
                          return_value=columns) as mock_process_columns, (
                patch.object(self.graph_maker, 'plot_graph')
                ) as mock_plot_graph:
            self.graph_maker.run('def')
            mock_process_columns.assert_called_once()
            mock_plot_graph.assert_called_once_with(columns)

        with patch.object(self.graph_maker, 'process_columns',
                          return_value=columns) as mock_process_columns, (
                patch.object(self.graph_maker, 'plot_graph')
                ) as mock_plot_graph:
            self.graph_maker.run('d')
            mock_process_columns.assert_called_once()
            mock_plot_graph.assert_called_once_with(columns)

        with patch.object(self.graph_maker, 'process_columns',
                          return_value=columns) as mock_process_columns, (
                patch.object(self.graph_maker, 'plot_graph')
                ) as mock_plot_graph:
            self.graph_maker.run('deflt')
            mock_process_columns.assert_called_once()
            mock_plot_graph.assert_called_once_with(columns)

    def test_run_interactive_mode(self):
        """
        Test if the run method correctly calls the interactive_mode method when
        the interactive mode is specified.

        Steps:
        1. Create a mock for the interactive_mode method.
        2. Call the run method of the GraphMaker instance with the interactive
           mode.
        3. Assert that the interactive_mode method was called once.
        """
        with patch.object(self.graph_maker, 'interactive_mode') as \
             mock_interactive_mode:
            self.graph_maker.run('interactive')
            mock_interactive_mode.assert_called_once()

        with patch.object(self.graph_maker, 'interactive_mode') as \
             mock_interactive_mode:
            self.graph_maker.run('int')
            mock_interactive_mode.assert_called_once()

        with patch.object(self.graph_maker, 'interactive_mode') as \
             mock_interactive_mode:
            self.graph_maker.run('i')
            mock_interactive_mode.assert_called_once()

        with patch.object(self.graph_maker, 'interactive_mode') as \
             mock_interactive_mode:
            self.graph_maker.run('inteactive')
            mock_interactive_mode.assert_called_once()

    def test_run_invalid_mode(self):
        """
        Test if the run method raises a ValueError when an invalid mode is
        specified.

        Steps:
        1. Call the run method of the GraphMaker instance with an invalid mode.
        2. Assert that a ValueError is raised.
        """
        with self.assertRaises(ValueError):
            self.graph_maker.run('test')


class Test_GraphMaker_interactive_mode(unittest.TestCase):
    """
    Test case for the interactive_mode method of the GraphMaker class.
    """

    def setUp(self):
        """
        Set up test data and objects.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        self.test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(self.test_df)

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    def test_interactive_mode_exit(self, mock_print, mock_input):
        """
        Test if the interactive_mode method exits correctly.
        The expected behavior is that the interactive_mode method exits when
        the user types 'exit'.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Call the interactive_mode method of the GraphMaker instance.
        4. Assert that the print and input functions were called with the
           expected arguments.
        """

        calls = [
            call('The following quantities have been found: mass, distance, '
                 'time, energy, velocity'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Exiting the loop...')
        ]

        self.graph_maker.interactive_mode()

        mock_input.assert_called_with(
            'Select which quantities to display and how: '
        )
        mock_print.assert_has_calls(calls, any_order=False)

    @patch('builtins.input', side_effect=['Display [mass, energy]', 'exit'])
    @patch('builtins.print')
    @patch.object(GraphMaker, 'plot_graph')
    def test_interactive_mode_display_mode(
        self, mock_plot_graph, mock_print, mock_input
    ):
        """
        Test if the interactive_mode method calls the plot_graph method with
        the correct arguments when the user selects Display mode.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Call the interactive_mode method of the GraphMaker instance.
        4. Assert that the plot_graph method was called with the correct
           arguments.
        5. Assert that the print and input functions were called with the
           expected arguments.
        """

        calls = [
            call('The following quantities have been found: mass, '
                 'distance, time, energy, velocity'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Exiting the loop...')
            ]

        self.graph_maker.interactive_mode()

        mock_print.assert_has_calls(calls, any_order=False)
        mock_plot_graph.assert_called_with(['energy'])

    @patch('builtins.input', side_effect=['Combine [mass, energy]', 'exit'])
    @patch('builtins.print')
    @patch.object(GraphMaker, 'plot_graph')
    def test_interactive_mode_combine_mode(
        self, mock_plot_graph, mock_print, mock_input
    ):
        """
        Test if the interactive_mode method calls the plot_graph method with
        the correct arguments when the user selects Combine mode.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Call the interactive_mode method of the GraphMaker instance.
        4. Assert that the plot_graph method was called with the correct
           arguments.
        5. Assert that the print and input functions were called with the
           expected arguments.
        """

        calls = [
            call('The following quantities have been found: mass, '
                 'distance, time, energy, velocity'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Exiting the loop...')
            ]

        self.graph_maker.interactive_mode()

        mock_print.assert_has_calls(calls, any_order=False)
        mock_input.assert_called_with(
            'Select which quantities to display and how: '
        )
        mock_plot_graph.assert_called_with(['mass', 'energy'])

    @patch('builtins.input', side_effect=['Display (miss, test)', 'exit'])
    @patch('builtins.print')
    def test_interactive_mode_IndexError(self, mock_print, mock_input):
        """
        Test if an invalid input is provided to the interactive_mode method.
        The expected behavior is that the interactive_mode method handles an
        IndexError correctly when invalid input is provided.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Call the interactive_mode method of the GraphMaker instance.
        4. Assert that the print and input functions were called with the
           expected arguments.
        """

        calls = [
            call('The following quantities have been found: mass, distance, '
                 'time, energy, velocity'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Invalid input, try again.'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Exiting the loop...')
            ]

        self.graph_maker.interactive_mode()

        mock_input.assert_called_with(
            'Select which quantities to display and how: '
        )
        mock_print.assert_has_calls(calls, any_order=False)

    @patch('builtins.input', side_effect=['Display (miss, test]', 'exit'])
    @patch('builtins.print')
    def test_interactive_mode_ValueError(self, mock_print, mock_input):
        """
        Test if an invalid input is provided to the interactive_mode method.
        The expected behavior is that the interactive_mode method handles a
        ValueError correctly when invalid input is provided.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Call the interactive_mode method of the GraphMaker instance.
        4. Assert that the print and input functions were called with the
           expected arguments.
        """

        calls = [
            call('The following quantities have been found: mass, distance, '
                 'time, energy, velocity'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Invalid input, try again.'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Exiting the loop...')
            ]

        self.graph_maker.interactive_mode()

        mock_input.assert_called_with(
            'Select which quantities to display and how: '
        )
        mock_print.assert_has_calls(calls, any_order=False)

    @patch('builtins.input', side_effect=['Display [miss, test]', 'exit'])
    @patch('builtins.print')
    def test_interactive_mode_keyword_not_found(self, mock_print, mock_input):
        """
        Test if a keyword is not found in the interactive_mode method.
        The expected behavior is that the interactive_mode method handles a
        keyword not found error correctly.

        Steps:
        1. Create a test DataFrame with sample data and column names.
        2. Create an instance of the GraphMaker class with the test DataFrame.
        3. Call the interactive_mode method of the GraphMaker instance.
        4. Assert that the print and input functions were called with the
           expected arguments.
        """

        calls = [
            call('The following quantities have been found: mass, distance, '
                 'time, energy, velocity'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs.'
                 ' Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Invalid keywords, try again.'),
            call('Define printing settings:'),
            call('Input format: mode [q_name1, q_name2, q_name3]'),
            call('To exit the program type: "exit"'),
            call('Modes'),
            call('Display - Displays a multiple figures with all "Time vs. '
                 'Quantity" data plotted separately'),
            call('Combine - Displays a single figure with all "Time vs. '
                 'Quantity" data plotted together.'),
            call('Exiting the loop...')]

        self.graph_maker.interactive_mode()

        mock_input.assert_called_with(
            'Select which quantities to display and how: '
            )
        mock_print.assert_has_calls(calls, any_order=False)


class Test_GraphMaker_check_and_process_input(unittest.TestCase):
    """
    Test case for the check_and_process_input method of the GraphMaker class.
    """

    def setUp(self):
        """
        Set up test data and objects.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(test_df)

    def test_valid_input(self):
        """
        Test if the method correctly processes valid input.
        The expected behavior is that the method returns True for input_check,
        the correct mode, and the list of keywords.

        Steps:
        1. Create a valid input string.
        2. Call the check_and_process_input method of the GraphMaker instance
           with the valid input string.
        3. Assert that the returned values are correct.
        """
        graph_input = "display [mass, energy, velocity]"
        expected_mode = "display"
        expected_keywords = ["mass", "energy", "velocity"]


        input_check, mode, keywords_list = self.graph_maker.check_and_process_input(graph_input)

        self.assertTrue(input_check)
        self.assertEqual(mode, expected_mode)
        self.assertEqual(keywords_list, expected_keywords)

    def test_invalid_input_missing_brackets(self):
        """
        Test if the method correctly handles input with missing brackets.
        The expected behavior is that the method returns False for input_check
        and an empty list for keywords_list.

        Steps:
        1. Create an input string with missing brackets.
        2. Call the check_and_process_input method of the GraphMaker instance
           with the input string.
        3. Assert that the returned values are correct.
        """
        graph_input = "display mass, energy, velocity"

        input_check, mode, keywords_list = self.graph_maker.check_and_process_input(graph_input)

        self.assertFalse(input_check)
        self.assertEqual(keywords_list, [])

    def test_invalid_input_empty_keywords(self):
        """
        Test if the method correctly handles input with empty keywords.
        The expected behavior is that the method returns True for input_check,
        the correct mode, and a list with an empty string for keywords_list.

        Steps:
        1. Create an input string with empty keywords.
        2. Call the check_and_process_input method of the GraphMaker instance
           with the input string.
        3. Assert that the returned values are correct.
        """
        graph_input = "display []"
        expected_mode = "display"
        expected_keywords = ['']

        input_check, mode, keywords_list = self.graph_maker.check_and_process_input(graph_input)

        self.assertTrue(input_check)
        self.assertEqual(mode, expected_mode)
        self.assertEqual(keywords_list, expected_keywords)

    def test_invalid_input_missing_mode(self):
        """
        Test if the method correctly handles input with missing mode.
        The expected behavior is that the method returns True for input_check
        and an empty list for keywords_list.

        Steps:
        1. Create an input string with missing mode.
        2. Call the check_and_process_input method of the GraphMaker instance
           with the input string.
        3. Assert that the returned values are correct.
        """
        graph_input = "[mass, energy, velocity]"

        input_check, mode, keywords_list = self.graph_maker.check_and_process_input(graph_input)

        self.assertTrue(input_check)
        self.assertEqual(keywords_list, ['mass', 'energy', 'velocity'])

    def test_invalid_input_missing_mode_and_brackets(self):
        """
        Test if the method correctly handles input with missing mode and brackets.
        The expected behavior is that the method returns False for input_check
        and an empty list for keywords_list.

        Steps:
        1. Create an input string with missing mode and brackets.
        2. Call the check_and_process_input method of the GraphMaker instance
           with the input string.
        3. Assert that the returned values are correct.
        """
        graph_input = "mass, energy, velocity"

        input_check, mode, keywords_list = self.graph_maker.check_and_process_input(graph_input)

        self.assertFalse(input_check)
        self.assertEqual(keywords_list, [])


class Test_GraphMaker_check_keywords(unittest.TestCase):
    """
    Test case for the check_keywords method of the GraphMaker class.
    """

    def setUp(self):
        """
        Set up test data and objects.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        self.test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(self.test_df)

    def test_check_keywords_valid(self):
        """
        Test if the check_keywords method returns True for valid keywords.
        The expected behavior is that the method returns True when provided
        with a list of keywords that exist as columns in the DataFrame.

        Steps:
        1. Create a list of valid keywords.
        2. Call the check_keywords method of the GraphMaker instance with the
           list of valid keywords.
        3. Assert that the returned value is True.
        """
        valid_keywords = ['mass', 'distance', 'time']
        self.assertTrue(self.graph_maker.check_keywords(valid_keywords))

    def test_check_keywords_invalid(self):
        """
        Test if the check_keywords method returns False for invalid keywords.
        The expected behavior is that the method returns False when provided
        with a list of keywords that do not exist as columns in the DataFrame.

        Steps:
        1. Create a list of invalid keywords.
        2. Call the check_keywords method of the GraphMaker instance with the
           list of invalid keywords.
        3. Assert that the returned value is False.
        """
        invalid_keywords = ['force', 'pressure', 'temperature']
        self.assertFalse(self.graph_maker.check_keywords(invalid_keywords))


class Test_GraphMaker_select_graph_mode(unittest.TestCase):
    """
    Test case for the select_graph_mode method of the GraphMaker class.
    """

    def setUp(self):
        """
        Set up test data and objects.
        """
        data = [[1, 2, 3, 4, 5]]
        keywords = ['mass', 'distance', 'time', 'energy', 'velocity']
        self.test_df = pd.DataFrame(data, columns=keywords)
        self.graph_maker = GraphMaker(self.test_df)

    @patch.object(GraphMaker, 'plot_graph')
    def test_select_graph_mode_display(self, mock_plot_graph):
        """
        Test if the select_graph_mode method calls the plot_graph method with
        the correct arguments when the mode is 'display'.

        Steps:
        1. Create an instance of the GraphMaker class with a test DataFrame.
        2. Call the select_graph_mode method with mode='display' and a list of
           keywords.
        3. Assert that the plot_graph method is called with each keyword in the
           list of keywords.
        """
        keywords_list = ['mass', 'energy', 'velocity']
        self.graph_maker.select_graph_mode('display', keywords_list)
        expected_calls = [call(['mass']), call(['energy']), call(['velocity'])]
        mock_plot_graph.assert_has_calls(expected_calls)

    @patch.object(GraphMaker, 'plot_graph')
    def test_select_graph_mode_combine(self, mock_plot_graph):
        """
        Test if the select_graph_mode method calls the plot_graph method with
        the correct arguments when the mode is 'combine'.

        Steps:
        1. Create an instance of the GraphMaker class with a test DataFrame.
        2. Call the select_graph_mode method with mode='combine' and a list of
           keywords.
        3. Assert that the plot_graph method is called with the list of
           keywords.
        """
        keywords_list = ['mass', 'energy', 'velocity']
        self.graph_maker.select_graph_mode('combine', keywords_list)
        mock_plot_graph.assert_called_once_with(keywords_list)


if __name__ == '__main__':
    unittest.main()
