"""Functions to process the data from Firebase
	Future things to do: make classes to formate firebase data and pass it in formated so my funcation can be poly
"""
from firebase import firebase

from geopy.distance import vincenty

# Connects to the public transit API
transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

def gets_a_dic_of_vehicle(bus_line):
	"""Takes in a bus line and returns a dictionary of vehicle ids that are in the line
	    output:{u'5488': True, 
	         	u'5604': True, 
	         	...  
	         	u'5525': True}
	"""
	line = bus_line
	available_buses = transit_firebase.get("sf-muni/routes/", line)
	return available_buses


def sorts_bus_dic_by_distance(bus_dictionary):
	"""With a list of buses from a line, it'll pull out the real time latitude and longitude and 
	calucates the distance from Powell Station"""
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


powell_station = (37.7846810, -122.4073680)