"""Connects to my firebase jazz"""

from firebase import firebase

from geopy.distance import vincenty

import time


# sets me up with the transit firebase
firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)


################# get all the routes that are avialble:
# routes_info = firebase.get("sf-muni/routes", None)

# for route in routes_info:
# 	print route
# 	print "~" * 100 

# gets all the available buses for a line:


line = "N"
available_buses = firebase.get("sf-muni/routes/", line)


print "avaiable vehicles: ", available_buses


available_vehicle_with_direction = []
direction = "O"

for vehicle in available_buses:
	vehicle_id = vehicle
	print "vehicle id ", vehicle_id
	try:
		vehicle_dirTag = firebase.get("sf-muni/vehicles/" + vehicle_id, "dirTag")
		print "vehicle dirtag ", vehicle_dirTag
		if vehicle_dirTag:
			vehicle_value_direction = vehicle_dirTag.find(direction)
			print "vehicle value direction ", vehicle_value_direction
			if vehicle_dirTag.find(direction) != -1:
				available_vehicle_with_direction.append(vehicle)
				print "the list so far ", available_vehicle_with_direction
	except AttributeError:
			pass


# for bus in available_buses:
# 	print bus
# 	print "~"*100

# print "actual items", available_buses


# #lat, lon
# print "~" * 100


powell_station = (37.7846810, -122.4073680)
# gets the vehicle infom for the available buses:
tuples_lat_lon_vehicle = []
for bus in available_vehicle_with_direction:
	bus_id = bus
	bus_lat = firebase.get("sf-muni/vehicles/" + bus_id, "lat")
	bus_lon = firebase.get("sf-muni/vehicles/" + bus_id, "lon")
	geolocation = (bus_lat, bus_lon)
	distance = (vincenty(powell_station, geolocation).miles)
	# print "bus id: ", bus_id
	# print "bus lat: ", bus_lat
	# print "bus lon: ", bus_lon
	# print "geolocation: ", geolocation
	# print "vincenty: ", distance
	# print "~" * 25
	if bus_lat != None:
		tuples_lat_lon_vehicle.append(tuple([distance, bus_id]))

# print "my tuples", tuples_lat_lon_vehicle
# print "~" * 80
sortedtups = sorted(tuples_lat_lon_vehicle)
print "sorted", sortedtups



time.sleep(60)

tuples_lat_lon_vehicle2 = []
for bus in available_buses:
	bus_id = bus
	bus_lat = firebase.get("sf-muni/vehicles/" + bus_id, "lat")
	bus_lon = firebase.get("sf-muni/vehicles/" + bus_id, "lon")
	geolocation = (bus_lat, bus_lon)
	distance = (vincenty(powell_station, geolocation).miles)
	# print "bus id: ", bus_id
	# print "bus lat: ", bus_lat
	# print "bus lon: ", bus_lon
	# print "geolocation: ", geolocation
	# print "vincenty: ", distance
	# print "~" * 25
	if bus_lat != None:
		tuples_lat_lon_vehicle2.append(tuple([distance, bus_id]))

# print "my tuples", tuples_lat_lon_vehicle2
# print "~" * 80
sortedtups2 = sorted(tuples_lat_lon_vehicle2)
print "sorted", sortedtups2




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

# recieves a list of tuples with vincity distane, bus ids

# ~~~~~~~~~~~~~~~~~~~~~~~to double check the vincity to user ~~~~

# vv = (Vincenty, Vehicle_id)
# while(vehicle_id_flag = False):
# 	for vv2 in range(len(sortedtups2)):
# 		for vv1 in range(len(sortedtups)):
# 			if sortedtups2[vv2][1] == sortedtups[vv1][1]:
# 				if sortedtups2[vv2][0] <= sortedtups[vv1][0]:
# 					vehicle_id = sortedtups2[vv2][1]
# 					print "This one won!", sortedtups2[vv2][1]
# 					vehicle_id_flag = True
# 					break
# 				elif vehicle_id_flag == True:
# 					break
# 			elif vehicle_id_flag == True:
# 					break
# 		elif vehicle_id_flag == True:
# 					break
# 	elif vehicle_id_flag == True:
# 					break

class BreakIt(Exception): pass

vehicle_id_closest = -1
print "vehicle id closest before trying: ", vehicle_id_closest

print "this is sortedtups: ", sortedtups
print "this is sortedtups2: ", sortedtups2

try:
    for vv2 in range(len(sortedtups2)):
    	print "for loop, vv2: ", vv2
    	for vv1 in range(len(sortedtups)):
			print "for loop, vv1: ", vv1
			print "vehicle in list 2: ", sortedtups2[vv2][1]
			print "vehicle in list 2, distance: ", sortedtups2[vv2][0]
			print "vehicle in list 1: ", sortedtups[vv1][1]
			if sortedtups2[vv1][1] == sortedtups[vv1][1]:
				if sortedtups2[vv2][0] <= sortedtups[vv1][0]:
					vehicle_id_closest = sortedtups2[vv2][1]
					print "This one won!", vehicle_id_closest
                	raise BreakIt
except BreakIt:
    pass



	# vehicle_id_closest_backup = sortedtups2[1][1]
	# print "this one didn't win, but its the closest", vehicle_id_closest
print "vehicle id closest aftering trying: ", vehicle_id_closest

try: 
	if vehicle_id_closest == -1:
		vehicle_id_closest = sortedtups2[0][1]
		vehicle_id_closest2 = sortedtups2[1][0]
		print "didn't win, but went with: ", vehicle_id_closest
except IndexError:
	pass

print "this is my vehicle for the trip: ", vehicle_id_closest
	# bus_lat = firebase.get("sf-muni/vehicles/" + vehicle_id_closest, "lat")
	# bus_lon = firebase.get("sf-muni/vehicles/" + vehicle_id_closest, "lon")
	# geolocation = (bus_lat, bus_lon)
	# distance = (vincenty(powell_station, geolocation).miles)

	# bus_lat_backup = firebase.get("sf-muni/vehicles/" + vehicle_id_closest_backup, "lat")
	# bus_lon_backup = firebase.get("sf-muni/vehicles/" + vehicle_id_closest_backup, "lon")
	# geolocation_backup = (bus_lat_backup, bus_lon_backup)
	# distance_backup = (vincenty(powell_station, geolocation_backup).miles)

	# if distance > distance_backup:
	# 	vehicle_id_closest = vehicle_id_closest_backup
	# 	print "vehicle_id", vehicle_id_closest


# for num in range(len(sortedtups)):
# 	if sortedtups2[0][1] == sortedtups[num][1]:
# 		if sortedtups2[0][0] <= sortedtups[num][0]:
# 			print "sortedtups2[0] won!", sortedtups2[0]
# 			vehicle_id = sortedtups2[0][1]
# 		else:
# 			print "didn't find it"
# 			print "sortedtups[num]", sortedtups[num]
# 			print "sortedtups2[0]", sortedtups2[0]
# 			for num in range(len(sortedtups)):
# 				if sortedtups2[1][1] == sortedtups[num][1]:
# 					if sortedtups2[1][0] <= sortedtups[num][0]:
# 						print "sortedtups2[1] won!", sortedtups2[1]
# 						vehicle_id = sortedtups2[1][1]
# 					else:
# 						for num in range(len(sortedtups)):
# 							if sortedtups2[2][1] == sortedtups[num][1]:
# 								if sortedtups2[2][0] <= sortedtups[num][0]:
# 									print "sortedtups2[2] won!", sortedtups2[1]
# 									vehicle_id = sortedtups2[2][1]

# vehicle_list1 = [(0.12315312469250524, u'1426'), (0.12315312469250524, u'1438'), (0.4675029273179666, u'1520'), (0.4675029273179666, u'1539'), (0.4926871038219716, u'1484')]
# vehicle_list2 = [[(0.016675650192621124, u'1426'), (0.048622709177496184, u'1438'), (0.3983583482037339, u'1484'), (0.5805606158286056, u'1539'), (0.6169215360786691, u'1520')]
		
# def selects_closest_vehicle(vehicle_list1, vehicle_list2):
# 	vehicle_id_1 = vehicle_list1[0][1]
# 	vehicle_id_2 = vehicle_list1[1][1]
# 	vehicle_id_3 = vehicle_list1[2][0]


# 	vehicle_lat = firebase.get("sf-muni/vehicles/" + vehicle_id, "lat")
# 	vehicle_lon = firebase.get("sf-muni/vehicles/" + vehicle_id, "lon")
# 	vehicle_geolocation = (vehicle_lat, vehicle_lon)
# 	distance = (vincenty(whole_foods, vehicle_geolocation).miles)


WALK_RADIUS = .25
# the distance that the average person walks to a transit stop that city developers 
# & transit use to space out their stops, currently sent to 1/4 mile



home_geolocation = (37.7615535,-122.4720836)
whole_foods = (37.7713951,-122.4295542)

x = 0

while (x < 20):
	vehicle_lat = firebase.get("sf-muni/vehicles/" + vehicle_id_closest, "lat")
	vehicle_lon = firebase.get("sf-muni/vehicles/" + vehicle_id_closest, "lon")
	vehicle_geolocation = (vehicle_lat, vehicle_lon)
	distance = (vincenty(whole_foods, vehicle_geolocation).miles)
	if vehicle_geolocation == None:
		print "What should I do? I'm not keeping track of where the last one was at, hmm"
	if distance <= WALK_RADIUS:
		print "my vehicle is ", distance
		print "my vehicle geolocation: ", vehicle_geolocation
		print "my vehicle is near my home"
		break
	print "my vehicle is ", distance
	print "my vehicle geolocation: ", vehicle_geolocation
	x += 1
	time.sleep(30)

print "Done"






