""" Functions to process the data from Firebase"""

def sorts_buslist_by_distance(user_lat, user_lon, buslist):
	distance_list = []
	for bus in buslist:
		lat_distance = user_lat - bus["lat"]
		lon_distance = user_lon - bus["lon"]
		bus_id = bus["id"]
		distance_list.append((lat_distance, lon_distance, bus_id))
	return distance_list