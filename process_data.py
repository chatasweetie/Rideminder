"""Functions to process the data"""
from firebase import firebase
from geopy.distance import vincenty
from time import sleep
import phonenumbers
import simplejson, urllib
import json
import pprint
import os 
import time
import datetime


GOOGLE_MAP_API_KEY= os.environ.get("GOOGLE_MAP_API_KEY")

# Connects to the public transit API
transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

# these are for I am working in python -i to play with my functions
user_lat= 37.785152
user_lon = -122.406581
destination_lat = 37.762028
destination_lon = -122.470790
bound = "O"
line = "N"


def convert_to_e164(raw_phone):
	"""formats phone numbers to twilio format

		>>> convert_to_e164("383.239.2280")
		u'+13832392280'

		>>> convert_to_e164("(934)234-2384")
		u'+19342342384'

	"""
	if not raw_phone:
		return
	if raw_phone[0] == '+':
		# Phone number may already be in E.164 format.
		parse_type = None
	else:
		# If no country code information present, assume it's a US number
		parse_type = "US"

	phone_representation = phonenumbers.parse(raw_phone, parse_type)

	return phonenumbers.format_number(phone_representation,
        phonenumbers.PhoneNumberFormat.E164)


def gets_a_list_of_available_line():
	"""gets all the available lines from firebase into a list

		>>> gets_a_list_of_available_line()
		[u'1', u'10', u'12', u'14', u'14R', u'14X', u'18', u'19', u'1AX', u'1BX', u'2', u'21', u'22', u'23', u'24', u'25', u'27', u'28', u'28R', u'29', u'3', u'30', u'30X', u'31', u'31AX', u'31BX', u'33', u'35', u'36', u'37', u'38', u'38AX', u'38BX', u'38R', u'39', u'41', u'43', u'44', u'45', u'47', u'48', u'49', u'5', u'52', u'54', u'55', u'56', u'57', u'59', u'5R', u'6', u'60', u'61', u'66', u'67', u'7', u'7R', u'7X', u'8', u'81X', u'82X', u'88', u'89', u'8AX', u'8BX', u'9', u'9R', u'F', u'J', u'KT', u'K_OWL', u'L', u'L_OWL', u'M', u'M_OWL', u'N', u'NX', u'N_OWL', u'T', u'T_OWL']

	runtime = O(n)
	"""

	available_lines = []
	
	available_lines_raw = transit_firebase.get("sf-muni/", "routes")

	for line in available_lines_raw:
		available_lines.append(line)
	
	return sorted(available_lines)


def gets_a_dic_of_vehicle(line):
	"""Takes in a vehicle line and returns a dictionary of vehicle ids that are in the line
	    
	output example: {u'5488': True, u'5604': True, ... u'5525': True}

	    >>> gets_a_dic_of_vehicle("N") # doctest: +ELLIPSIS
		{u'...': True, ... u'...': True}

	runtime = O(n)
	"""
	available_vehicles = transit_firebase.get("sf-muni/routes/", line)
	
	return available_vehicles


def validates_bound_direction_of_vehicles_in_line(dic_vehicles_for_line, bound_dir):
	"""From a dictionary of vehicles in a line, it'll filter for the ones going the 
	correct bound direction: "O" = Outboud, "I" = Inboud

	output example: [u'1481', u'1486', ... u'1513']

		>>> dic = gets_a_dic_of_vehicle("N")
		>>> validates_bound_direction_of_vehicles_in_line(dic, bound)
		[u'...', u'...', ... u'...']

	runtime = O(n)
	"""
	available_vehicle_with_direction = []
	bound = bound_dir

	for vehicle in dic_vehicles_for_line:
		vehicle_id = vehicle
		try:
			vehicle_dirTag = transit_firebase.get("sf-muni/vehicles/" + 
				vehicle_id, "dirTag")
			if vehicle_dirTag:
				if vehicle_dirTag.find(bound) != -1:
					available_vehicle_with_direction.append(vehicle)
		except AttributeError:
			pass

	return available_vehicle_with_direction


def gets_geolocation_of_a_vehicle(vehicle_id):
	"""With the vehicle id, it gets from firebase the current latitude and longitude
	of the vehicle and returns it as a geolocation

	example output: (37.73831, -122.46859)

		>>> print gets_geolocation_of_a_vehicle(1403)# doctest: +ELLIPSIS
		(..., ...)

	O(1)
	"""
	vehicle_id = str(vehicle_id)

	try:
		vehicle_lat = transit_firebase.get("sf-muni/vehicles/" + vehicle_id, "lat")
		vehicle_lon = transit_firebase.get("sf-muni/vehicles/" + vehicle_id, "lon")
		vehicle_geolocation = (vehicle_lat, vehicle_lon)
	except AttributeError:
		vehicle_geolocation = None 

	return vehicle_geolocation


def sorts_vehicles_dic_by_distance(vehicle_dictionary, user_lat, user_lon):
	"""With a list of vehicles from a line, it'll pull out the real time latitude and longitude and 
	calucates the distance from the user_geolocation. Returns a sorted list of tuples:

	example output: [(0.4675029273179666, u'1491'), (0.9429363612471457, u'1486'), ... (7956.1553552570285, u'1446')]

		>>> user_lat= 37.7846810
		>>> user_lon = -122.4073680
		>>> vehicles = [u'1481', u'1486', u'1485', u'1520', u'1422', u'1427', u'1548', u'1502', u'1446', u'1468', u'1440', u'1476', u'1462', u'1491', u'1493', u'1497', u'1498', u'1537', u'1510', u'1513']
		>>> sorts_vehicles_dic_by_distance(vehicles, user_lat, user_lon)
		[(..., u'...'), (..., u'...'), ... (..., u'...')]

		"""

	user_geolocation = (user_lat,user_lon)
	tuples_lat_lon_vehicle = []

	for vehicle in vehicle_dictionary:
		vehicle_id = vehicle
		vehicle_geolocation = gets_geolocation_of_a_vehicle(vehicle_id)
		if vehicle_geolocation is not None:
						# vincenity is the distance between two geolocations that 
						# takes into account the sphereness of the world
			distance = (vincenty(user_geolocation, vehicle_geolocation).miles)
			tuples_lat_lon_vehicle.append(tuple([distance, vehicle_id]))
	vehicles_sorted_by_vincenity = sorted(tuples_lat_lon_vehicle)
	
	return vehicles_sorted_by_vincenity

# Removed becasue heroku timed out
#TODO: make sorts_vehicle_dic_by_distance process faster
# def selects_closest_vehicle(vehicle_list1, vehicle_list2):
# 	"""From two list of (distance, vehicle id), returns the closest vehicleid.

# 	Compares the vincity distance of the first vehicle of the first dictionary to the 
# 	second dictionary to validate if its getting smaller (closer), if not then validates 
# 	the second vehicle distance.

# 		>>> vehicle_list1 = [(0.12315312469250524, u'1426'), (0.12315312469250524, u'1438'), (0.4675029273179666, u'1520'), (0.4675029273179666, u'1539'), (0.4926871038219716, u'1484')]
# 		>>> vehicle_list2 = [(0.016675650192621124, u'1426'), (0.048622709177496184, u'1438'), (0.3983583482037339, u'1484'), (0.5805606158286056, u'1539'), (0.6169215360786691, u'1520')]
# 		>>> print selects_closest_vehicle(vehicle_list1, vehicle_list2)
# 		1426

# 	O(n^2)
# 	"""
# 	# if the sorting vehicles cannot determine the closest bus, it'll be catch in the "try"
# 	vehicle_id = -1
# 
# 	# vv = (Vincenty, Vehicle_id)
# 	for vv2 in range(5):
# 		for vv1 in range(5):
# 			if vehicle_list1[vv2][1] == vehicle_list1[vv1][1]:
# 				if vehicle_list1[vv2][0] <= vehicle_list1[vv1][0]:
# 					vehicle_id = vehicle_list1[vv2][1]
# 					return vehicle_id
# 	try: 
# 		if vehicle_id == -1:
# 			vehicle_id = vehicle_list2[0][1]
# 			vehicle_id2 = vehicle_list2[1][0]

# 	except IndexError:
# 		pass

# 	return vehicle_id

	
def processes_line_and_bound_selects_closest_vehicle(line, bound, destination_lat, destination_lon, user_lat, user_lon):
	""""With a line and bound direction(O = Outbound, I=Inbound), it'll get the 
	list of vehicles on the line and gets the vehicle's geolocation twice (a 
	minute a part) and compares the distance to make sure that the vehicle is 
	actually coming to my user

	example output: u'1529'

		>>> processes_line_and_bound_selects_closest_vehicle(line, bound, destination_lat, destination_lon, user_lat, user_lon) # doctest: +ELLIPSIS
		u'...'

	"""

	print "step 0"
	dic_vehicles_for_line = gets_a_dic_of_vehicle(line)
	print "step 1"
	bounded_vehicles_for_line = validates_bound_direction_of_vehicles_in_line(dic_vehicles_for_line,bound)
	print "step 2"
	list_of_vincenty_first = sorts_vehicles_dic_by_distance(bounded_vehicles_for_line, user_lat, user_lon)
	# Removed to make process faster for heroku error 12 (timeout)
	# print "step 3"
	# sleep(30)
	# print "step 4"
	# list_of_vincenty_second = sorts_vehicles_dic_by_distance(bounded_vehicles_for_line, user_lat, user_lon)
	# print "step 5"
	# vehicle_id = selects_closest_vehicle(list_of_vincenty_first,list_of_vincenty_second)
	# print "step 6"
	vehicle_id = list_of_vincenty_first[0][1]

	return vehicle_id


def gets_rawjson_with_lat_lon(user_lat, user_lon, destination_lat, destination_lon):
	"""makes a call to gogole map to get the json data of two geolocations"""

	orig_coord = user_lat, user_lon
	dest_coord = destination_lat, destination_lon

	url = "https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&departure_time=now&traffic_model=best_guess&mode=transit&key={2}".format(str(orig_coord),str(dest_coord),str(GOOGLE_MAP_API_KEY))
	result= simplejson.load(urllib.urlopen(url))

	googleResponse = urllib.urlopen(url)
	jsonResponse = json.loads(googleResponse.read())

	return jsonResponse


def rawjson_into_datetime(rawjson):
	"""parses out json to get of arrival time and turn it into datetime"""

	arrival_time_raw =rawjson['routes'][0]['legs'][0]['arrival_time']['text']
	arrival_time_raw_split = arrival_time_raw.split(":")

	# This is so line 264 has sometime to reference to
	arrival_time_hour = 0 

	if arrival_time_raw[-2:] == "pm":
		arrival_time_hour = 12
		
	arrival_time_hour += int(arrival_time_raw_split[0])
	arrival_time_min = arrival_time_raw_split[1][:-2]

	hours = int(arrival_time_hour)
	minutes = int(arrival_time_min)

	now = datetime.datetime.now()

	arrival_time = now.replace(hour=hours, minute=minutes)

	return arrival_time


def process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_lat, destination_lon):
	"""takes in geolocations and returns the arrival time in datatime when the transit is completed"""

	rawjson = gets_rawjson_with_lat_lon(user_lat, user_lon, destination_lat, destination_lon)
	print rawjson
	arrival_time = rawjson_into_datetime(rawjson)

	return arrival_time





