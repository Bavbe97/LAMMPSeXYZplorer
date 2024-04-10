import pandas as pd
import matplotlib.pyplot as plt
from lammpshade.Constructor import *


UNITS_MAPPING = {
            'real': {
                    'mass': r'(g/mol)',
                    'distance': r'($/AA$)',
                    'time': r'(fs)',
                    'energy': r'$(kcal/mol)$',
                    'velocity': r'($\AA$ / fs)',
                    'force': r'$((kcal/mol)/\AA)$',
                    'torque': r'$(kcal/mol)$',
                    'temperature': r'(K)',
                    'pressure': r'(atm)',
                    'dynamic viscosity': r'(P)',
                    'charge': r'm. of e. c.',
                    'dipole': r'(charge \times \AA)$',
                    'electric field': r'$(V/\AA)$',
                    'density': r'($g/cm^\text{dim}$)'
            },
            'metal': {
                    'mass': r'$\frac{\text{g}}{\text{mol}}$',
                    'distance': r'\AA',
                    'time': r'ps',
                    'energy': r'eV',
                    'velocity': r'$\frac{\text{\AA}}{\text{ps}}$',
                    'force': r'$\frac{\text{eV}}{\text{\AA}}$',
                    'torque': r'eV',
                    'temperature': r'K',
                    'pressure': r'bar',
                    'dynamic viscosity': r'P',
                    'charge': r'multiple of electron charge (1.0 is a proton)',
                    'dipole': r'$\text{charge}\times\text{\AA}$',
                    'electric field': r'V/\text{\AA}',
                    'density': r'$\frac{\text{g}}{\text{cm}^\text{dim}}$'
            }}


class GraphMaker:
    """
    A class that represents a graph maker.

    Attributes:
        df (pandas.DataFrame): The DataFrame containing data.
    
    Methods:
        __init__(self, df): Initializes the GraphMaker object.
    """

    def __init__(self, df):
        """
        Initializes the GraphMaker object.

        Args:
            df (pandas.DataFrame): The DataFrame containing data.

        Raises:
            ValueError: If df is empty.

        Returns:
            None
        """
        if df.empty:
            raise ValueError('Data cannot be empty')
        self.df = df

