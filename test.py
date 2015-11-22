"""To Unit test then Integration Test my Transit Alert Application"""
import unittest
import doctest
from process_data import convert_to_e164, gets_a_list_of_available_line, selects_closest_vehicle, gets_a_dic_of_vehicle



class UnitTestTwillioTestCase(unittest.TestCase):
	def test_convert_to_e164(self):
		self.assertEqual(convert_to_e164("(843)323-2343"), u'+18433232343')


class UnitTestTransitData(unittest.TestCase):
	def test_gets_a_list_of_available_line(self):
		self.assertTrue(gets_a_list_of_available_line() > 64)

	def setUp(self):
		"""Creating mock firebase to test aganist"""

	# 	def _mock_transit_firebase():
	# 		return "CA"

	# 	# self._old_transit_firebase = process_data.transit_firebase
	# 	process_data.transit_firebase = _mock_transit_firebase

	# def test_amount_gets_a_dic_of_vehicle(self):
	# 	self.assertTrue(gets_a_dic_of_vehicle("N") > 30)

	# def test_gets_a_dic_of_vehicle(self):
	# 	self.assertEqual(gets_a_dic_of_vehicle("N"), "CA")

	def test_selects_closest_vehicle(self):
		self.assertEqual(selects_closest_vehicle([(0.9338186621320413, u'1472'), (0.9338186621320413, u'1488'), (1.0398499771587593, u'1455'), (1.0498968948022667, u'1548'), (1.0620705886593063, u'1542'), (1.0644210057899908, u'1528'), (1.0687742887784755, u'1431'), (2.8519879512450164, u'1495'), (4.1161739909827215, u'1535'), (4.820269824445265, u'1459'), (4.890819705827765, u'1442'), (4.893685411614527, u'1519'), (6.297064411922732, u'1476')], [(1.031659187344977, u'1455'), (1.0580960246268907, u'1548'), (1.0626269823073644, u'1528'), (1.0687742887784755, u'1431'), (1.074272454517364, u'1542'), (1.1370610262790521, u'1472'), (1.1370610262790521, u'1488'), (2.739059251454709, u'1495'), (4.219898289028735, u'1535'), (4.819294276261407, u'1459'), (4.890819705827765, u'1442'), (4.893685411614527, u'1519'), (6.303176742628762, u'1476')]), '1472')








# transit_firebase.get("sf-muni/routes/", line)

	# def test_gets_a_dic_of_vehicle(self, "N"):




# self.client = firebase.test_client()

# gets_a_list_of_available_line():
# class 



# class TestStringMethods(unittest.TestCase):

#   def test_upper(self):
#       self.assertEqual('foo'.upper(), 'FOO')

#   def test_isupper(self):
#       self.assertTrue('FOO'.isupper())
#       self.assertFalse('Foo'.isupper())

#   def test_split(self):
#       s = 'hello world'
#       self.assertEqual(s.split(), ['hello', 'world'])
#       # check that s.split fails when the separator is not a string
#       with self.assertRaises(TypeError):
#           s.split(2)





if __name__ == '__main__':
    unittest.main()




