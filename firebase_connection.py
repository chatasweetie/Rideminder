"""Connects to my firebase jazz"""

from firebase import firebase


# sets me up with the transit firebase
firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

# gets route infomration from firebase transit
route_info = firebase.get("sf-muni/routes", None)

print "Route Information: ",route_info

# gets vehicle information
vehicle_1418 = firebase.get("sf-muni/vehicles/1418", None)

print "Vehicle 1418 Information: ",vehicle_1418

# gets latitude for specific vehicle 
lat_vehicle_1418 = firebase.get("sf-muni/vehicles/1418", "lat")

print "Vehicle 1418 Latitutde: ",lat_vehicle_1418