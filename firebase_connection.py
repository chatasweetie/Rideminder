"""Connects to my firebase jazz"""

from firebase import firebase

from geopy.distance import vincenty



# sets me up with the transit firebase
firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)


################# get all the routes that are avialble:
# routes_info = firebase.get("sf-muni/routes", None)

# for route in routes_info:
# 	print route
# 	print "~" * 100 

# gets all the available buses for a line:
available_buses = firebase.get("sf-muni/routes/", "1")

for bus in available_buses:
	print bus
	print "~"*100

print "actual items", available_buses


#lat, lon
print "~" * 100


powell_station = (37.7846810, -122.4073680)
# gets the vehicle infom for the available buses:
tuples_lat_lon_vehicle = []
for bus in available_buses:
	bus_id = bus
	bus_lat = firebase.get("sf-muni/vehicles/" + bus_id, "lat")
	bus_lon = firebase.get("sf-muni/vehicles/" + bus_id, "lon")
	geolocation = (bus_lat, bus_lon)
	distance = (vincenty(powell_station, geolocation).miles)
	print "bus id: ", bus_id
	print "bus lat: ", bus_lat
	print "bus lon: ", bus_lon
	print "geolocation: ", geolocation
	print "vincenty: ", distance
	print "~" * 25
	if bus_lat != None:
		tuples_lat_lon_vehicle.append(tuple([distance, bus_id]))

print "my tuples", tuples_lat_lon_vehicle
sortedtups = sorted(tuples_lat_lon_vehicle)
print "sorted", sortedtups







#to get vehicle information with variable bus number! 
# bus_id = str(1418)
# vehicle_1418 = firebase.get("sf-muni/vehicles/" + bus_id, None)
# print vehicle_1418



# # gets route infomration from firebase transit
# route_info = firebase.get("sf-muni/routes", None)

# print "Route Information: ",route_info

# # gets vehicle information
# vehicle_1418 = firebase.get("sf-muni/vehicles/1418", None)

# print "Vehicle 1418 Information: ",vehicle_1418

# # gets latitude for specific vehicle 
# lat_vehicle_1418 = firebase.get("sf-muni/vehicles/1418", "lat")

# print "Vehicle 1418 Latitutde: ",lat_vehicle_1418

# # print outs all the vehicles
# routes_heading_num = firebase.get("sf-muni/vehicles", None)

# for route in routes_heading_num:
# 	print route
# 	print "~" * 100

# print "Routes Heading Number: ",routes_heading_num

