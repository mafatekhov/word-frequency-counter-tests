import unittest

from lab1_frequences_counter import main

class CountFrequenciesTest(unittest.TestCase):
	def test_dummy(self):
		res = main.calculate_frequences('')
		self.assertEqual(res, 0)
