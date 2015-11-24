"""To Unit test then Integration Test my Transit Alert Application"""
import unittest
from unittest import TestCase
import doctest
from process_data import convert_to_e164, gets_a_list_of_available_line, selects_closest_vehicle, gets_a_dic_of_vehicle, validates_bound_direction_of_vehicles_in_line, gets_geolocation_of_a_vehicle, sorts_vehicles_dic_by_distance, selects_closest_vehicle, processes_line_and_bound_selects_closest_vehicle
from firebase import firebase
import process_data
# import tasks
# from task import process_transit_request
from server import app
import server
from model import Transit_Request
from flask_sqlalchemy import SQLAlchemy

# to test:
# python test.py
# coverage:
# coverage run --source=. test.py
# for report:
# coverage report -m

db = SQLAlchemy()

########################################################
def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests."""

    tests.addTests(doctest.DocTestSuite(server))
    tests.addTests(doctest.DocFileSuite("tests.txt"))
    return tests

########################################################
class UnitTestTwillioTestCase(unittest.TestCase):
	def test_convert_to_e164(self):
		self.assertEqual(convert_to_e164("(843)323-2343"), u'+18433232343')
		print "complete phone number convertion test"

########################################################
class UnitTestTransitData(unittest.TestCase):
	def test_gets_a_list_of_available_line(self):
		self.assertTrue(gets_a_list_of_available_line() > 64)
		print "complete gets a list of aviable lines test "

	def test_selects_closest_vehicle(self):
		print "testing the selects_closest_vehicle"
		self.assertEqual(selects_closest_vehicle([(0.9338186621320413, u'1472'), (0.9338186621320413, u'1488'), (1.0398499771587593, u'1455'), (1.0498968948022667, u'1548'), (1.0620705886593063, u'1542'), (1.0644210057899908, u'1528'), (1.0687742887784755, u'1431'), (2.8519879512450164, u'1495'), (4.1161739909827215, u'1535'), (4.820269824445265, u'1459'), (4.890819705827765, u'1442'), (4.893685411614527, u'1519'), (6.297064411922732, u'1476')], [(1.031659187344977, u'1455'), (1.0580960246268907, u'1548'), (1.0626269823073644, u'1528'), (1.0687742887784755, u'1431'), (1.074272454517364, u'1542'), (1.1370610262790521, u'1472'), (1.1370610262790521, u'1488'), (2.739059251454709, u'1495'), (4.219898289028735, u'1535'), (4.819294276261407, u'1459'), (4.890819705827765, u'1442'), (4.893685411614527, u'1519'), (6.303176742628762, u'1476')]), '1472')

########################################################
class UnitTestMockData(unittest.TestCase):
	"""Testing wit Mock Data"""
	print"got into mock data class"

	def setUp(self):
		"""Creating mock firebase to test aganist"""
		mock_transit_firebase = firebase.FirebaseApplication("https://popping-torch-2216.firebaseio.com/sf-muni", None)

		self._old_transit_firebase = process_data.transit_firebase
		process_data.transit_firebase = mock_transit_firebase

	def tearDown(self):
		"""Resets my firebase to its normal one"""
		process_data.transit_firebase = self._old_transit_firebase


	def test_gets_a_dic_of_vehicle(self):
		results = {u'1426': u'True', u'1410': u'True', u'1402': u'True', u'1413': u'True', u'1415': u'True', u'1404': u'True'}
		self.assertEqual(gets_a_dic_of_vehicle("N"), results)

	def test_validates_bound_direction_of_vehicles_in_line(self):
		dic = gets_a_dic_of_vehicle("N")
		results = [u'1426', u'1410', u'1402', u'1413', u'1415']
		self.assertEqual(validates_bound_direction_of_vehicles_in_line(dic, "O"), results)

	def test_validates_bound_direction_not_be(self):
		dic = gets_a_dic_of_vehicle("N")
		negative_results = "1404"
		self.assertNotEqual(validates_bound_direction_of_vehicles_in_line(dic, "O"), negative_results)

	def test_gets_geolocation_of_a_vehicle(self):
		self.assertEqual(gets_geolocation_of_a_vehicle(1402),(37.7213, -122.46912))

	def test_sorts_vehicles_dic_by_distance(self):
		dic = gets_a_dic_of_vehicle("N")
		bound_dic = validates_bound_direction_of_vehicles_in_line(dic, "O")
		results = [(0.9313235948899348, u'1426'), (4.275886490639952, u'1415'), (4.7115931592023585, u'1410'), (5.526469350242915, u'1402'), (5.59359790362578, u'1413')]
		self.assertEqual(sorts_vehicles_dic_by_distance(bound_dic, 37.7846810, -122.4073680), results)

	def test_selects_closest_vehicle(self): 
		vehicle_list1 = [(0.12315312469250524, u'1426'), (0.12315312469250524, u'1438'), (0.4675029273179666, u'1520'), (0.4675029273179666, u'1539'), (0.4926871038219716, u'1484')]
		vehicle_list2 = [(0.016675650192621124, u'1426'), (0.048622709177496184, u'1438'), (0.3983583482037339, u'1484'), (0.5805606158286056, u'1539'), (0.6169215360786691, u'1520')]
		self.assertEqual(selects_closest_vehicle(vehicle_list1, vehicle_list2), "1426")

	def test_processes_line_and_bound_selects_closest_vehicle(self):
		user_lat= 37.7846810
		user_lon = -122.4073680
		destination_lat = 37.7846810
		destination_lon = -122.4073680
		bound = "O"
		line = "N"
		results = "1426"
		self.assertEqual(processes_line_and_bound_selects_closest_vehicle(line, bound, destination_lat, destination_lon, user_lat, user_lon), results)

########################################################
class UnitTestMockDataForCelery(unittest.TestCase):
	"""Testing wit Mock Data"""
	print"got into mock data class for celery"

	def setUp(self):
		"""Creating mock firebase to test aganist"""
		mock_transit_firebase = firebase.FirebaseApplication("https://popping-torch-2216.firebaseio.com/sf-muni", None)

		self._old_transit_firebase = tasks.transit_firebase
		tasks.transit_firebase = mock_transit_firebase

	def tearDown(self):
		"""Resets my firebase to its normal one"""
		tasks.transit_firebase = self._old_transit_firebase

	# def test_process_transit_request(self):
		# How to test if twilio worked?



# class IntergrationServerTest(unittest.TestCase):
# 	"""Integration Test: testing flask sever"""

# 	# def setUp(self):
# 	# 	print "(setUp ran for SeverTest w/example_data.db)"
# 	# 	self.client = server.app.test_client()

# 	# 	connect_to_db(app, "sqlite:///example_data.db")

# 	# 	db.create_all()
# 	# 	example_data()

# 	def test_home(self):
# 		print "testing homepage"
# 		expected_homepage = '<!doctype html>\n<html>\n    <head>\n      <title>Transit Alert</title>\n      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">\n      <meta name="viewport" content="width=device-width, initial-scale=1">\n      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">\n    <link rel="stylesheet" type="text/css" href="/static/css/styling.css">\n    \n  <script src="http://maps.google.com/maps/api/js"></script>\n\n\n    </head>\n\n<body>\n    <div class="container-fluid">\n        <p class="navbar-brand">Transit Alert</p>\n      </div>\n    </div><!-- /.container-fluid -->\n\n\n\n  <hr>\n\n  \n\n<div class="row">\n  <div clase="row">\n  <div class="container">\n    <p> Awesome_Name is a messaging system that will notify user when their transit vehicle is within three blocks of their destination via text message.<b><em> * Required for processsing </b></em> </p>\n  </div>\n  <div class="container">\n    <form class="col-sm-2 control-label" id="transit_request" action="/user_input" method="POST">\n      <div class="form-group">\n        <label for="fname"> Name</label>\n        <input type="text" class="form-control" name="fname" placeholder="optional">\n      </div>\n<!--       <div class="form-group">\n        <label for="lname">Last Name</label>\n        <input type="text" class="form-control" name="lname" placeholder="optional">\n      </div> -->\n      <div class="form-group">\n        <label for="email">Email</label>\n        <input type="email" class="form-control" name="email" placeholder="optional">\n      </div>\n      <div class="form-group">\n        <label for="phone"><em>Phone Number*</em></label>\n        <!-- http://bootstrapformhelpers.com/phone/ -->\n        <input type="text" class="form-control bfh-phone" value="(555)555-5555" data-format="+1 (ddd) ddd-dddd" name="phone">\n      </div>\n      <div class="form-group">\n        <label for="line"><em>Transit Line*</em></label>\n          <select class="form-control" id="line" name="line">\n            \n            <option>1</option>\n            \n            <option>10</option>\n            \n            <option>12</option>\n            \n            <option>14</option>\n            \n            <option>14R</option>\n            \n            <option>14X</option>\n            \n            <option>18</option>\n            \n            <option>19</option>\n            \n            <option>1AX</option>\n            \n            <option>1BX</option>\n            \n            <option>2</option>\n            \n            <option>21</option>\n            \n            <option>22</option>\n            \n            <option>23</option>\n            \n            <option>24</option>\n            \n            <option>27</option>\n            \n            <option>28</option>\n            \n            <option>28R</option>\n            \n            <option>29</option>\n            \n            <option>3</option>\n            \n            <option>30</option>\n            \n            <option>30X</option>\n            \n            <option>31</option>\n            \n            <option>31AX</option>\n            \n            <option>31BX</option>\n            \n            <option>33</option>\n            \n            <option>35</option>\n            \n            <option>36</option>\n            \n            <option>37</option>\n            \n            <option>38</option>\n            \n            <option>38AX</option>\n            \n            <option>38BX</option>\n            \n            <option>38R</option>\n            \n            <option>39</option>\n            \n            <option>41</option>\n            \n            <option>43</option>\n            \n            <option>44</option>\n            \n            <option>45</option>\n            \n            <option>47</option>\n            \n            <option>48</option>\n            \n            <option>49</option>\n            \n            <option>5</option>\n            \n            <option>52</option>\n            \n            <option>54</option>\n            \n            <option>55</option>\n            \n            <option>56</option>\n            \n            <option>57</option>\n            \n            <option>59</option>\n            \n            <option>5R</option>\n            \n            <option>6</option>\n            \n            <option>60</option>\n            \n            <option>61</option>\n            \n            <option>66</option>\n            \n            <option>67</option>\n            \n            <option>7</option>\n            \n            <option>76X</option>\n            \n            <option>7R</option>\n            \n            <option>7X</option>\n            \n            <option>8</option>\n            \n            <option>81X</option>\n            \n            <option>82X</option>\n            \n            <option>88</option>\n            \n            <option>89</option>\n            \n            <option>8AX</option>\n            \n            <option>8BX</option>\n            \n            <option>9</option>\n            \n            <option>9R</option>\n            \n            <option>E</option>\n            \n            <option>F</option>\n            \n            <option>J</option>\n            \n            <option>KT</option>\n            \n            <option>K_OWL</option>\n            \n            <option>L</option>\n            \n            <option>L_OWL</option>\n            \n            <option>M</option>\n            \n            <option>M_OWL</option>\n            \n            <option>N</option>\n            \n            <option>NX</option>\n            \n            <option>N_OWL</option>\n            \n            <option>T</option>\n            \n            <option>T_OWL</option>\n            \n          </select>\n      </div>\n      <div class="form-group">\n        <label for="bound"><em>Direction*</em></label>\n          <select class="form-control" id="bound" name="bound">\n            <option value="I">Inbound</option>\n            <option value="O">Outbound</option>\n          </select>\n      </div>\n      <div class="form-group">\n        <label for="destination"><em>Available Stops*</em></label>\n          <select class="form-control"name="destination" id="stops">\n            <!-- this is where $ and Ajax adds the stop options             -->\n          </select>\n      </div>\n\n      <button type="submit" class="btn btn-default">Submit</button>\n    </form>\n    <div class="col-sm-10">\n      <div id="transitmap">\n        \n      </div>\n\n      <!-- my map will live here -->\n    </div> <!-- closes form -->\n  </div> <!-- closes container -->\n</div> <!-- closes row -->\n\n</div>\n\n\n<script src="http://code.jquery.com/jquery.js"></script>\n<script src="/static/javascript/scripts.js"></script>\n<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>\n\n\n\n\n</body>\n</html>'
# 		result = self.client.get("/")
# 		self.assertIn(expected_homepage, result.data)

# 	def test_thankyou(self):
# 		# expected_thankyou = '<!doctype html>\n<html>\n    <head>\n      <title>Transit Alert</title>\n      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">\n      <meta name="viewport" content="width=device-width, initial-scale=1">\n      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">\n    <link rel="stylesheet" type="text/css" href="/static/css/styling.css">\n    \n  <script src="http://maps.google.com/maps/api/js"></script>\n\n\n    </head>\n\n<body>\n    <div class="container-fluid">\n        <p class="navbar-brand">Transit Alert</p>\n      </div>\n    </div><!-- /.container-fluid -->\n\n\n\n  <hr>\n\n  \n\n<div class="row">\n  <div clase="row">\n  <div class="container">\n    <p> Awesome_Name is a messaging system that will notify user when their transit vehicle is within three blocks of their destination via text message.<b><em> * Required for processsing </b></em> </p>\n  </div>\n  <div class="container">\n    <form class="col-sm-2 control-label" id="transit_request" action="/user_input" method="POST">\n      <div class="form-group">\n        <label for="fname"> Name</label>\n        <input type="text" class="form-control" name="fname" placeholder="optional">\n      </div>\n<!--       <div class="form-group">\n        <label for="lname">Last Name</label>\n        <input type="text" class="form-control" name="lname" placeholder="optional">\n      </div> -->\n      <div class="form-group">\n        <label for="email">Email</label>\n        <input type="email" class="form-control" name="email" placeholder="optional">\n      </div>\n      <div class="form-group">\n        <label for="phone"><em>Phone Number*</em></label>\n        <!-- http://bootstrapformhelpers.com/phone/ -->\n        <input type="text" class="form-control bfh-phone" value="(555)555-5555" data-format="+1 (ddd) ddd-dddd" name="phone">\n      </div>\n      <div class="form-group">\n        <label for="line"><em>Transit Line*</em></label>\n          <select class="form-control" id="line" name="line">\n            \n            <option>1</option>\n            \n            <option>10</option>\n            \n            <option>12</option>\n            \n            <option>14</option>\n            \n            <option>14R</option>\n            \n            <option>14X</option>\n            \n            <option>18</option>\n            \n            <option>19</option>\n            \n            <option>1AX</option>\n            \n            <option>1BX</option>\n            \n            <option>2</option>\n            \n            <option>21</option>\n            \n            <option>22</option>\n            \n            <option>23</option>\n            \n            <option>24</option>\n            \n            <option>27</option>\n            \n            <option>28</option>\n            \n            <option>28R</option>\n            \n            <option>29</option>\n            \n            <option>3</option>\n            \n            <option>30</option>\n            \n            <option>30X</option>\n            \n            <option>31</option>\n            \n            <option>31AX</option>\n            \n            <option>31BX</option>\n            \n            <option>33</option>\n            \n            <option>35</option>\n            \n            <option>36</option>\n            \n            <option>37</option>\n            \n            <option>38</option>\n            \n            <option>38AX</option>\n            \n            <option>38BX</option>\n            \n            <option>38R</option>\n            \n            <option>39</option>\n            \n            <option>41</option>\n            \n            <option>43</option>\n            \n            <option>44</option>\n            \n            <option>45</option>\n            \n            <option>47</option>\n            \n            <option>48</option>\n            \n            <option>49</option>\n            \n            <option>5</option>\n            \n            <option>52</option>\n            \n            <option>54</option>\n            \n            <option>55</option>\n            \n            <option>56</option>\n            \n            <option>57</option>\n            \n            <option>59</option>\n            \n            <option>5R</option>\n            \n            <option>6</option>\n            \n            <option>60</option>\n            \n            <option>61</option>\n            \n            <option>66</option>\n            \n            <option>67</option>\n            \n            <option>7</option>\n            \n            <option>76X</option>\n            \n            <option>7R</option>\n            \n            <option>7X</option>\n            \n            <option>8</option>\n            \n            <option>81X</option>\n            \n            <option>82X</option>\n            \n            <option>88</option>\n            \n            <option>89</option>\n            \n            <option>8AX</option>\n            \n            <option>8BX</option>\n            \n            <option>9</option>\n            \n            <option>9R</option>\n            \n            <option>E</option>\n            \n            <option>F</option>\n            \n            <option>J</option>\n            \n            <option>KT</option>\n            \n            <option>K_OWL</option>\n            \n            <option>L</option>\n            \n            <option>L_OWL</option>\n            \n            <option>M</option>\n            \n            <option>M_OWL</option>\n            \n            <option>N</option>\n            \n            <option>NX</option>\n            \n            <option>N_OWL</option>\n            \n            <option>T</option>\n            \n            <option>T_OWL</option>\n            \n          </select>\n      </div>\n      <div class="form-group">\n        <label for="bound"><em>Direction*</em></label>\n          <select class="form-control" id="bound" name="bound">\n            <option value="I">Inbound</option>\n            <option value="O">Outbound</option>\n          </select>\n      </div>\n      <div class="form-group">\n        <label for="destination"><em>Available Stops*</em></label>\n          <select class="form-control"name="destination" id="stops">\n            <!-- this is where $ and Ajax adds the stop options             -->\n          </select>\n      </div>\n\n      <button type="submit" class="btn btn-default">Submit</button>\n    </form>\n    <div class="col-sm-10">\n      <div id="transitmap">\n        \n      </div>\n\n      <!-- my map will live here -->\n    </div> <!-- closes form -->\n  </div> <!-- closes container -->\n</div> <!-- closes row -->\n\n</div>\n\n\n<script src="http://code.jquery.com/jquery.js"></script>\n<script src="/static/javascript/scripts.js"></script>\n<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>\n\n\n\n\n</body>\n</html>' not found in '<!doctype html>\n<html>\n    <head>\n      <title>\xef\x88\x87 fa-bus [&#xf207;] Transit Alert</title>\n      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">\n      <meta name="viewport" content="width=device-width, initial-scale=1">\n      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">\n    <link rel="stylesheet" type="text/css" href="/static/css/styling.css">\n    \n  <script src="http://maps.google.com/maps/api/js"></script>\n\n\n    </head>\n\n<body>\n    <div class="container-fluid">\n        <p class="navbar-brand">Transit Alert</p>\n      </div>\n    </div><!-- /.container-fluid -->\n\n\n\n  <hr>\n\n  \n\n<div class="row">\n  <div clase="row">\n  <div class="container">\n    <p> Awesome_Name is a messaging system that will notify user when their transit vehicle is within three blocks of their destination via text message.<b><em> * Required for processsing </b></em> </p>\n  </div>\n  <div class="container">\n    <form class="col-sm-2 control-label" id="transit_request" action="/user_input" method="POST">\n      <div class="form-group">\n        <label for="fname"> Name</label>\n        <input type="text" class="form-control" name="fname" placeholder="optional">\n      </div>\n<!--       <div class="form-group">\n        <label for="lname">Last Name</label>\n        <input type="text" class="form-control" name="lname" placeholder="optional">\n      </div> -->\n      <div class="form-group">\n        <label for="email">Email</label>\n        <input type="email" class="form-control" name="email" placeholder="optional">\n      </div>\n      <div class="form-group">\n        <label for="phone"><em>Phone Number*</em></label>\n        <!-- http://bootstrapformhelpers.com/phone/ -->\n        <input type="text" class="form-control bfh-phone" value="(555)555-5555" data-format="+1 (ddd) ddd-dddd" name="phone">\n      </div>\n      <div class="form-group">\n        <label for="line"><em>Transit Line*</em></label>\n          <select class="form-control" id="line" name="line">\n            \n            <option>1</option>\n            \n            <option>10</option>\n            \n            <option>12</option>\n            \n            <option>14</option>\n            \n            <option>14R</option>\n            \n            <option>14X</option>\n            \n            <option>18</option>\n            \n            <option>19</option>\n            \n            <option>1AX</option>\n            \n            <option>1BX</option>\n            \n            <option>2</option>\n            \n            <option>21</option>\n            \n            <option>22</option>\n            \n            <option>23</option>\n            \n            <option>24</option>\n            \n            <option>25</option>\n            \n            <option>27</option>\n            \n            <option>28</option>\n            \n            <option>28R</option>\n            \n            <option>29</option>\n            \n            <option>3</option>\n            \n            <option>30</option>\n            \n            <option>30X</option>\n            \n            <option>31</option>\n            \n            <option>31AX</option>\n            \n            <option>31BX</option>\n            \n            <option>33</option>\n            \n            <option>35</option>\n            \n            <option>36</option>\n            \n            <option>37</option>\n            \n            <option>38</option>\n            \n            <option>38AX</option>\n            \n            <option>38BX</option>\n            \n            <option>38R</option>\n            \n            <option>39</option>\n            \n            <option>41</option>\n            \n            <option>43</option>\n            \n            <option>44</option>\n            \n            <option>45</option>\n            \n            <option>47</option>\n            \n            <option>48</option>\n            \n            <option>49</option>\n            \n            <option>5</option>\n            \n            <option>52</option>\n            \n            <option>54</option>\n            \n            <option>55</option>\n            \n            <option>56</option>\n            \n            <option>57</option>\n            \n            <option>59</option>\n            \n            <option>5R</option>\n            \n            <option>6</option>\n            \n            <option>60</option>\n            \n            <option>61</option>\n            \n            <option>66</option>\n            \n            <option>67</option>\n            \n            <option>7</option>\n            \n            <option>7R</option>\n            \n            <option>7X</option>\n            \n            <option>8</option>\n            \n            <option>81X</option>\n            \n            <option>82X</option>\n            \n            <option>83X</option>\n            \n            <option>88</option>\n            \n            <option>89</option>\n            \n            <option>8AX</option>\n            \n            <option>8BX</option>\n            \n            <option>9</option>\n            \n            <option>9R</option>\n            \n            <option>F</option>\n            \n            <option>J</option>\n            \n            <option>KT</option>\n            \n            <option>K_OWL</option>\n            \n            <option>L</option>\n            \n            <option>L_OWL</option>\n            \n            <option>M</option>\n            \n            <option>M_OWL</option>\n            \n            <option>N</option>\n            \n            <option>NX</option>\n            \n            <option>N_OWL</option>\n            \n            <option>T</option>\n            \n            <option>T_OWL</option>\n            \n          </select>\n      </div>\n      <div class="form-group">\n        <label for="bound"><em>Direction*</em></label>\n          <select class="form-control" id="bound" name="bound">\n            <option value="I">Inbound</option>\n            <option value="O">Outbound</option>\n          </select>\n      </div>\n      <div class="form-group">\n        <label for="destination"><em>Available Stops*</em></label>\n          <select class="form-control"name="destination" id="stops">\n            <!-- this is where $ and Ajax adds the stop options             -->\n          </select>\n      </div>\n\n      <button type="submit" class="btn btn-default">Submit</button>\n    </form>\n    <div class="col-sm-10">\n      <div id="transitmap">\n        \n      </div>\n\n      <!-- my map will live here -->\n    </div> <!-- closes form -->\n  </div> <!-- closes container -->\n</div> <!-- closes row -->\n\n</div>\n\n\n<script src="http://code.jquery.com/jquery.js"></script>\n<script src="/static/javascript/scripts.js"></script>\n<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>\n\n\n\n\n</body>\n</html>'
# 		result = self.client.get("/user_input")
# 		print "this is the results", results
# 		self.assertIn(expected_thankyou, result.data)

# 	def test_results(self):
# 		result = self.client.get("/")
# 		self.assertEqual(result.status_code, 200)


# class Transit_RequestTest(TestCase):
# 	"""Unit test about transit request"""

# 	def setUp(self):
# 		"""connects to database"""
# 		connect_to_db(app)

# 	def test_transitrequest_to_dic(self):
# 		"""Can transit request turn to dictionary?"""
# 		request1 = Transit_Request(id=1)
# 		expected = ""
# 		self.assertDictEqual(request1.to_dict(), expected)


# class FlaskTest(TestCase):
# 	def setUp(self):
# 		# Get the Flask test client
# 		self.client = app.test_client()

#         # Connect to temporary database
#         connect_to_db(app)

#         # Create tables and add sample data
#         db.create_all()
#         # example_data()


	def test_find_transit_request(self):
		"""Finds transit request that have been completed"""






	# transit_firebase.get("sf-muni/routes/", line)

	# def test_gets_a_dic_of_vehicle(self, "N"):




# self.client = firebase.test_client()

# gets_a_list_of_available_line():
# class 

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example_data.db'
    db.app = app
    db.init_app(app)



if __name__ == '__main__':
    unittest.main()
    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."



