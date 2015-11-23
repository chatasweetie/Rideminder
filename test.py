"""To Unit test then Integration Test my Transit Alert Application"""
import unittest
from unittest import TestCase
import doctest
from process_data import convert_to_e164, gets_a_list_of_available_line, selects_closest_vehicle, gets_a_dic_of_vehicle
from server import app
import server
from model import connect_to_db, Transit_Request

# to test:
# coverage run --source=. test.py
# for report:
# coverage report -m


def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests."""

    tests.addTests(doctest.DocTestSuite(server))
    tests.addTests(doctest.DocFileSuite("tests.txt"))
    return tests


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



class IntergrationServerTest(unittest.TestCase):
	"""Integration Test: testing flask sever"""

	def setUp(self):
		print "(setUp ran)"
		self.client = server.app.test_client()


	def test_home(self):
		print "testing homepage"
		expected_homepage = '<!doctype html>\n<html>\n    <head>\n      <title>Transit Alert</title>\n      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">\n      <meta name="viewport" content="width=device-width, initial-scale=1">\n      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">\n    <link rel="stylesheet" type="text/css" href="/static/css/styling.css">\n    \n  <script src="http://maps.google.com/maps/api/js"></script>\n\n\n    </head>\n\n<body>\n    <div class="container-fluid">\n        <p class="navbar-brand">Transit Alert</p>\n      </div>\n    </div><!-- /.container-fluid -->\n\n\n\n  <hr>\n\n  \n\n<div class="row">\n  <div clase="row">\n  <div class="container">\n    <p> Awesome_Name is a messaging system that will notify user when their transit vehicle is within three blocks of their destination via text message.<b><em> * Required for processsing </b></em> </p>\n  </div>\n  <div class="container">\n    <form class="col-sm-2 control-label" id="transit_request" action="/user_input" method="POST">\n      <div class="form-group">\n        <label for="fname"> Name</label>\n        <input type="text" class="form-control" name="fname" placeholder="optional">\n      </div>\n<!--       <div class="form-group">\n        <label for="lname">Last Name</label>\n        <input type="text" class="form-control" name="lname" placeholder="optional">\n      </div> -->\n      <div class="form-group">\n        <label for="email">Email</label>\n        <input type="email" class="form-control" name="email" placeholder="optional">\n      </div>\n      <div class="form-group">\n        <label for="phone"><em>Phone Number*</em></label>\n        <!-- http://bootstrapformhelpers.com/phone/ -->\n        <input type="text" class="form-control bfh-phone" value="(555)555-5555" data-format="+1 (ddd) ddd-dddd" name="phone">\n      </div>\n      <div class="form-group">\n        <label for="line"><em>Transit Line*</em></label>\n          <select class="form-control" id="line" name="line">\n            \n            <option>1</option>\n            \n            <option>10</option>\n            \n            <option>12</option>\n            \n            <option>14</option>\n            \n            <option>14R</option>\n            \n            <option>14X</option>\n            \n            <option>18</option>\n            \n            <option>19</option>\n            \n            <option>1AX</option>\n            \n            <option>1BX</option>\n            \n            <option>2</option>\n            \n            <option>21</option>\n            \n            <option>22</option>\n            \n            <option>23</option>\n            \n            <option>24</option>\n            \n            <option>27</option>\n            \n            <option>28</option>\n            \n            <option>28R</option>\n            \n            <option>29</option>\n            \n            <option>3</option>\n            \n            <option>30</option>\n            \n            <option>30X</option>\n            \n            <option>31</option>\n            \n            <option>31AX</option>\n            \n            <option>31BX</option>\n            \n            <option>33</option>\n            \n            <option>35</option>\n            \n            <option>36</option>\n            \n            <option>37</option>\n            \n            <option>38</option>\n            \n            <option>38AX</option>\n            \n            <option>38BX</option>\n            \n            <option>38R</option>\n            \n            <option>39</option>\n            \n            <option>41</option>\n            \n            <option>43</option>\n            \n            <option>44</option>\n            \n            <option>45</option>\n            \n            <option>47</option>\n            \n            <option>48</option>\n            \n            <option>49</option>\n            \n            <option>5</option>\n            \n            <option>52</option>\n            \n            <option>54</option>\n            \n            <option>55</option>\n            \n            <option>56</option>\n            \n            <option>57</option>\n            \n            <option>59</option>\n            \n            <option>5R</option>\n            \n            <option>6</option>\n            \n            <option>60</option>\n            \n            <option>61</option>\n            \n            <option>66</option>\n            \n            <option>67</option>\n            \n            <option>7</option>\n            \n            <option>76X</option>\n            \n            <option>7R</option>\n            \n            <option>7X</option>\n            \n            <option>8</option>\n            \n            <option>81X</option>\n            \n            <option>82X</option>\n            \n            <option>88</option>\n            \n            <option>89</option>\n            \n            <option>8AX</option>\n            \n            <option>8BX</option>\n            \n            <option>9</option>\n            \n            <option>9R</option>\n            \n            <option>E</option>\n            \n            <option>F</option>\n            \n            <option>J</option>\n            \n            <option>KT</option>\n            \n            <option>K_OWL</option>\n            \n            <option>L</option>\n            \n            <option>L_OWL</option>\n            \n            <option>M</option>\n            \n            <option>M_OWL</option>\n            \n            <option>N</option>\n            \n            <option>NX</option>\n            \n            <option>N_OWL</option>\n            \n            <option>T</option>\n            \n            <option>T_OWL</option>\n            \n          </select>\n      </div>\n      <div class="form-group">\n        <label for="bound"><em>Direction*</em></label>\n          <select class="form-control" id="bound" name="bound">\n            <option value="I">Inbound</option>\n            <option value="O">Outbound</option>\n          </select>\n      </div>\n      <div class="form-group">\n        <label for="destination"><em>Available Stops*</em></label>\n          <select class="form-control"name="destination" id="stops">\n            <!-- this is where $ and Ajax adds the stop options             -->\n          </select>\n      </div>\n\n      <button type="submit" class="btn btn-default">Submit</button>\n    </form>\n    <div class="col-sm-10">\n      <div id="transitmap">\n        \n      </div>\n\n      <!-- my map will live here -->\n    </div> <!-- closes form -->\n  </div> <!-- closes container -->\n</div> <!-- closes row -->\n\n</div>\n\n\n<script src="http://code.jquery.com/jquery.js"></script>\n<script src="/static/javascript/scripts.js"></script>\n<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>\n\n\n\n\n</body>\n</html>'
		result = self.client.get('/')
		self.assertIn(expected_homepage, result.data)

	def test_thankyyou(self):
		expected_thankyou = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>405 Method Not Allowed</title>\n<h1>Method Not Allowed</h1>\n<p>The method is not allowed for the requested URL.</p>\n'
		result = self.client.get('/user_input')
		self.assertIn(expected_thankyou, result.data)


class Transit_RequestTest(TestCase):
	"""Unit test about transit request"""

	def setUp(self):
		"""connects to database"""
		connect_to_db(app)

	def test_transitrequest_to_dic(self):
		"""Can transit request turn to dictionary?"""
		request1 = Transit_Request(id=1)
		expected = ""
		self.assertDictEqual(request1.to_dict(), expected)


class FlaskTest(TestCase):
	def setUp(self):
		# Get the Flask test client
        self.client = app.test_client()

        # Connect to temporary database
        connect_to_db(app, "sqlite:///")

        # Create tables and add sample data
        db.create_all()
        example_data()


	def test_find_transit_request(self):
		"""Finds transit request that have been completed"""
		





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




