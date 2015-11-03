"""Functions to process the data from Firebase
	Future things to do: make classes to formate firebase data and pass it in formated so my funcation can be poly
"""
from firebase import firebase
from geopy.distance import vincenty
from time import sleep

# Connects to the public transit API
transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

def gets_a_dic_of_vehicle(bus_line):
	"""Takes in a bus line and returns a dictionary of vehicle ids that are in the line
	    output:{u'5488': True, 
	         	u'5604': True, 
	         	...  
	         	u'5525': True}
	    How to test when my list is always going to be different! AHH!
	"""
	line = bus_line
	available_buses = transit_firebase.get("sf-muni/routes/", line)
	return available_buses



def sorts_bus_dic_by_distance(bus_dictionary):
	"""With a list of buses from a line, it'll pull out the real time latitude and longitude and 
	calucates the distance from Powell Station. Returns a sorted list of tuples:

		returnse example:
		[(0.48780088356531986, u'5525'), (0.6690889326592107, u'5615'), ... (4.708043949446551, u'5507')]
			(vincenty, vehcile_id)

	"""
	tuples_lat_lon_vehicle = []
	powell_station = (37.7846810, -122.4073680)
	for bus in bus_dictionary:
		bus_id = bus
		bus_lat = transit_firebase.get("sf-muni/vehicles/" + bus_id, "lat")
		bus_lon = transit_firebase.get("sf-muni/vehicles/" + bus_id, "lon")
		bus_geolocation = (bus_lat, bus_lon)
		distance = (vincenty(powell_station, bus_geolocation).miles)
		if bus_lat != None:
			tuples_lat_lon_vehicle.append(tuple([distance, bus_id]))
	vehicles_sorted_by_vincenity = sorted(tuples_lat_lon_vehicle)
	return vehicles_sorted_by_vincenity

def selects_closest_vehicle(vehicle_list1, vehicle_list2):
	"""From two dictionaries of distance, vehicle id, returns the closest vehicleid
	Compares the vincity distance of the first vehicle of the first dictionary to the 
	second dictionary to validate if its getting smaller (closer), if not then validates 
	the second vehicle distance.
	example:
		vehicle_list1 = [(0.12315312469250524, u'1426'), (0.12315312469250524, u'1438'), (0.4675029273179666, u'1520'), (0.4675029273179666, u'1539'), (0.4926871038219716, u'1484')]
		vehicle_list2 = [[(0.016675650192621124, u'1426'), (0.048622709177496184, u'1438'), (0.3983583482037339, u'1484'), (0.5805606158286056, u'1539'), (0.6169215360786691, u'1520')]
		
	"""
	for num in range(len(vehicle_list1)):
		if vehicle_list2[0][1] == vehicle_list1[num][1]:
			if vehicle_list2[0][0] <= vehicle_list1[num][0]:
				return vehicle_list2[0][1]
			else:
				for num in range(len(sortedtups)):
					if sortedtups2[1][1] == sortedtups[num][1]:
						if sortedtups2[1][0] <= sortedtups[num][0]:
							return sortedtups2[1][1]

def processes_line_selects_closest_vehicle (line):
	dic_vehicles_for_line = gets_a_dic_of_vehicle(line)
	list_of_vincenty_first = sorts_bus_dic_by_distance(dic_vehicles_for_line)
	time.sleep(60)
	list_of_vincenty_second = sorts_bus_dic_by_distance(dic_vehicles_for_line)
	return selects_closest_vehicle(list_of_vincenty_first,list_of_vincenty_second)

powell_station = (37.7846810, -122.4073680)