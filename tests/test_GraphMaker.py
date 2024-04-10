import unittest
import pandas as pd
from lammpshade.GraphMaker import GraphMaker

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

if __name__ == '__main__':
    unittest.main()
