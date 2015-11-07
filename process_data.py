"""Functions to process the data from Firebase """
from firebase import firebase
from geopy.distance import vincenty
from time import sleep


# Connects to the public transit API
transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

WALK_RADIUS = .20
# the distance that the average person walks to a transit stop that city developers 
# & transit use to space out their stops, currently sent to 3 city block
line = "N"
bound = "O"
destination_geo_location = (37.7846810, -122.4073680)

def gets_a_list_of_available_line():
	"""gets all the available lines from firebase into a list

		>>> gets_a_list_of_avialbe_line()
		[u'56', u'54', u'43', u'60', u'61', u'31BX', u'49', u'66', u'67', u'1AX', u'KT', 
		...
		u'37', u'36', u'35', u'52', u'33', u'38R', u'48', u'5R', u'57', u'38BX']
	"""

	available_lines = []
	
	available_lines_raw = transit_firebase.get("sf-muni/", "routes")

	for line in available_lines_raw:
		available_lines.append(line)
	
	return sorted(available_lines)

def gets_a_dic_of_vehicle(line):
	"""Takes in a vehicle line and returns a dictionary of vehicle ids that are in the line
	    output:{u'5488': True, 
	         	u'5604': True, 
	         	...  
	         	u'5525': True}
	    How to test when my list is always going to be different! AHH!

	    >>> gets_a_dic_of_vehicle("N")
		{u'1530': True, u'1536': True, u'1483': True, u'1481': True, u'1486': True, 
		...
		u'1510': True, u'1513': True, u'1417': True}
	"""
	available_vehicles = transit_firebase.get("sf-muni/routes/", line)
	
	return available_vehicles

def validates_bound_direction_of_vehicles_in_line(dic_vehicles_for_line, bound_dir):
	"""From a dictionary of vehicles in a line, it'll filter for the ones going the 
	corrent bound direction, 
	O = Outboud, I = Inboud

		>>> dic = gets_a_dic_of_vehicle("N")
		>>> validates_bound_direction_of_vehicles_in_line(dic, "O")
		[u'1481', u'1486', u'1485', u'1520', u'1422', u'1427', u'1548', u'1502', 
		u'1446', u'1468', u'1440', u'1476', u'1462', u'1491', u'1493', u'1497', u'1498', 
		u'1537', u'1510', u'1513']
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
	of the vehicle and returns it as a geolocation"""
	try:
		vehicle_lat = transit_firebase.get("sf-muni/vehicles/" + vehicle_id, "lat")
		vehicle_lon = transit_firebase.get("sf-muni/vehicles/" + vehicle_id, "lon")
		vehicle_geolocation = (vehicle_lat, vehicle_lon)
	except AttributeError:
		vehicle_geolocation = None 

	return vehicle_geolocation


def sorts_vehicles_dic_by_distance(vehicle_dictionary, destination_geo_location):
	"""With a list of vehicles from a line, it'll pull out the real time latitude and longitude and 
	calucates the distance from Powell Station. Returns a sorted list of tuples:

		return example:
		[(0.48780088356531986, u'5525'), (0.6690889326592107, u'5615'), ... (4.708043949446551, u'5507')]
			(vincenty, vehcile_id)	"""

	tuples_lat_lon_vehicle = []
	for vehicle in vehicle_dictionary:
		vehicle_id = vehicle
		vehicle_geolocation = gets_geolocation_of_a_vehicle(vehicle_id)
		if vehicle_geolocation is not None:
			distance = (vincenty(destination_geo_location, vehicle_geolocation).miles)
			tuples_lat_lon_vehicle.append(tuple([distance, vehicle_id]))
	vehicles_sorted_by_vincenity = sorted(tuples_lat_lon_vehicle)
	
	return vehicles_sorted_by_vincenity

class BreakIt(Exception): pass
"""To be able to break out of nested loops"""


def selects_closest_vehicle(vehicle_list1, vehicle_list2):
	"""From two list of distance, vehicle id, returns the closest vehicleid
	Compares the vincity distance of the first vehicle of the first dictionary to the 
	second dictionary to validate if its getting smaller (closer), if not then validates 
	the second vehicle distance.
	example:
		vehicle_list1 = [(0.12315312469250524, u'1426'), (0.12315312469250524, u'1438'), (0.4675029273179666, u'1520'), (0.4675029273179666, u'1539'), (0.4926871038219716, u'1484')]
		vehicle_list2 = [[(0.016675650192621124, u'1426'), (0.048622709177496184, u'1438'), (0.3983583482037339, u'1484'), (0.5805606158286056, u'1539'), (0.6169215360786691, u'1520')]
		
	"""
	vehicle_id = -1
	try:
	    for vv2 in range(len(vehicle_list1)):
			for vv1 in range(len(vehicle_list1)):
				if vehicle_list1[vv2][1] == vehicle_list1[vv1][1]:
					if vehicle_list1[vv2][0] <= vehicle_list1[vv1][0]:
						vehicle_id = vehicle_list1[vv2][1]
	                	raise BreakIt
	except BreakIt:
		pass

	try: 
		if vehicle_id == -1:
			vehicle_id = vehicle_list2[0][1]
			vehicle_id2 = vehicle_list2[1][0]
	except IndexError:
		pass

	return vehicle_id


def processes_line_and_bound_selects_closest_vehicle(line, bound):
	""""With a line and bound direction(O = Outbound, I=Inbound), it'll get the 
	list of vehicles on the line and gets the vehicle's geolocation twice (a 
	minute a part) and compares the distance to make sure that the vehicle is 
	actually coming to my user"""

	dic_vehicles_for_line = gets_a_dic_of_vehicle(line)
	bounded_vehicles_for_line = validates_bound_direction_of_vehicles_in_line(dic_vehicles_for_line,bound)
	list_of_vincenty_first = sorts_vehicles_dic_by_distance(bounded_vehicles_for_line, destination_geo_location)
	sleep(60)
	list_of_vincenty_second = sorts_vehicles_dic_by_distance(bounded_vehicles_for_line, destination_geo_location)

	return selects_closest_vehicle(list_of_vincenty_first,list_of_vincenty_second)


def processes_queue():
	"""Checks the transit_request database to check if vehicle geolocation is within 
	thresold of users destination_geo_location"""
	in_query = list_of_queue_to_process()

	for request_id, vehicle_id, destination_geo_location in in_query:
		vehicle_geolocation = gets_geolocation_of_a_vehicle(vehicle_id)
		distance = (vincenty(destination_geo_location, vehicle_geolocation).miles)
		if distance <= WALK_RADIUS:
			# send alert!
			# edit is_finished to True
			print "All done"
			request_id.complete




