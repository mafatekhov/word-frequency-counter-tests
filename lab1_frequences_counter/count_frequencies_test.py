"""
Checks the first lab. Part about the creation of the frequencies dictionary
"""

import unittest

from lab1_frequences_counter import main


class CountFrequenciesTest(unittest.TestCase):
    """
    Tests dictionary creation
    """

    def test_dummy(self):
        """
        Ideal scenario
    	"""
        self.assertEqual(main.calculate_frequences(), 0)
