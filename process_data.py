"""Functions to process the data"""
from firebase import firebase
from geopy.distance import vincenty
import phonenumbers
import json
import os
import datetime
import requests


GOOGLE_MAP_API_KEY = os.environ.get("GOOGLE_MAP_API_KEY")

# Connects to the public transit API
transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

# these are for I am working in python -i to play with my functions
user_lat = 37.785152
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

    return phonenumbers.format_number(phone_representation, phonenumbers.PhoneNumberFormat.E164)


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
    """Takes in a vehicle line and returns a dictionary of vehicle ids that are in 
    current available on the transit line

    output example: {u'5488': True, u'5604': True, ... u'5525': True}

        >>> gets_a_dic_of_vehicle("N") # doctest: +ELLIPSIS
        {u'...': True, ... u'...': True}

    runtime = O(n)
    """
    available_vehicles = transit_firebase.get("sf-muni/routes/", line)

    return available_vehicles


def validates_bound_direction_of_vehicles_in_line(dic_vehicles_for_line, bound_dir):
    """From a dictionary of vehicles in a transit line, it'll filter for the ones going the 
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
    """With the vehicle id, it akes a call to firebase to get the the current latitude
    and longitude of the vehicle and returns it as a geolocation (lat, lon)

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


def selects_closest_vehicle(vehicle_1, vehicle_1_distance, vehicle_2, vehicle_2_distance, user_lat, user_lon):
    """From two vehicles (distance, vehicle id), returns the closest vehicleid.

    Compares the inital vincity distance of the first vehicle to an updated one to validate
    that the first vehicle is actually coming to the user (versus leaving the person).
    If its not correct, it'll check the second vehicle and validates it.

        >>> vehicle_1 = 1426
        >>> vehicle_1_distance = 0.12315312469250524
        >>> vehicle_2 = 1438
        >>> vehicle_2_distance = 0.12315312469250524
        >>> selects_closest_vehicle(vehicle_1, vehicle_1_distance, vehicle_2, vehicle_2_distance, user_lat, user_lon)
        1438

    """

    user_geolocation = (user_lat,user_lon)

    vehicle_geolocation = gets_geolocation_of_a_vehicle(vehicle_1)
    vehicle_1_distance_current = (vincenty(user_geolocation, vehicle_geolocation).miles)

    if vehicle_1_distance_current < vehicle_1_distance:
        return vehicle_1

    else:
        return vehicle_2


def processes_line_and_bound_selects_two_closest_vehicle(line, bound, destination_lat, destination_lon,
                                                            user_lat, user_lon):
    """"With a line and bound direction(O = Outbound, I=Inbound), it'll get the list of vehicles on
    the line and gets the vehicle's geolocation and returns to two closest vehicle distance and id

        >>> processes_line_and_bound_selects_two_closest_vehicle(line, bound, destination_lat, destination_lon,
        ...                                                             user_lat, user_lon)
        [(..., u'...'), (..., u'...'), ... (..., u'...')]

    """

    dic_vehicles_for_line = gets_a_dic_of_vehicle(line)
    bounded_vehicles_for_line = validates_bound_direction_of_vehicles_in_line(dic_vehicles_for_line, bound)
    sorted_list_of_vincenty = sorts_vehicles_dic_by_distance(bounded_vehicles_for_line, user_lat, user_lon)

    return sorted_list_of_vincenty[0:3]


def process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_lat, destination_lon):
    """takes in geolocations and returns the arrival time as a datatime object of when the
    transit is completed"""

    # this is to activate the Fixie proxy, so google direction api has the same ip address call
    proxyDict = {
              "http": os.environ.get('FIXIE_URL', ''),
              "https": os.environ.get('FIXIE_URL', '')
                }

    url = "https://maps.googleapis.com/maps/api/directions/json?origin={0},{1}&destination={2},{3}&departure_time=now&traffic_model=best_guess&mode=transit&key={4}".format(str(user_lat), str(user_lon), str(destination_lat), str(destination_lon), str(GOOGLE_MAP_API_KEY))

    r = requests.get(url, proxies=proxyDict)

    adict = r.json()
    print "adict", adict

    if "error_message" not in adict:

        arrival_time_raw = adict['routes'][0]['legs'][0]['arrival_time']['text']
        arrival_time_raw_split = arrival_time_raw.split(":")

        # This is so arrival_time_hour has sometime to reference to later in the code
        arrival_time_hour = 0

        if arrival_time_raw[-2:] == "pm":
            arrival_time_hour = 12

        arrival_time_hour += int(arrival_time_raw_split[0])
        arrival_time_min = arrival_time_raw_split[1][:-2]
        hours = int(arrival_time_hour)
        minutes = int(arrival_time_min)

        now = datetime.datetime.utcnow()

        arrival_time = now.replace(hour=hours, minute=minutes)

        return arrival_time

    return datetime.datetime.utcnow()
