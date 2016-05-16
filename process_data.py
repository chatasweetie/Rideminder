"""Functions to process the data"""
from firebase import firebase
from geopy.distance import vincenty
import phonenumbers
import json
import os
import datetime
import requests
from xml.etree import ElementTree
from model import Route_Stop, Agency, Route, Stop


GOOGLE_MAP_API_KEY = os.environ.get("GOOGLE_MAP_API_KEY")

TOKEN_511 = os.environ.get("TOKEN_511")

# Connects to the public transit API
transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

# these are for I am working in python -i to play with my functions
user_lat = 37.785152
user_lon = -122.406581
destination_lat = 37.762028
destination_lon = -122.470790
bound = "O"
line = "N"
agency = "BART"
route = "917"
RouteDirectionCode = ""
stop = "11"
user_stop = "30"
destination_stop = "95"


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
        # If no country code information present,
        # assume it's a US number
        parse_type = "US"

    phone_representation = phonenumbers.parse(raw_phone,
                                            parse_type)

    return phonenumbers.format_number(phone_representation,
                        phonenumbers.PhoneNumberFormat.E164)

# New Data processing
#############################################################
def gets_user_stop(user_lat, user_lon, agency, route, direction):
    """processes the lat/lon of user to find closest stop for their route

    returns stop.stop_code

    """

    route_stop = Route_Stop.query.filter_by(route_id=route)

    user_geolocation = (user_lat,user_lon)
    stops_vincenty_diff = []

    for rs in route_stop:
        stop_lat = rs.stop.lat
        stop_lon = rs.stop.lon
        stop_code = rs.stop.stop_code
        stop_geolocation = (lat, lon)

        # vincenity is the distance between two geolocations that
        # takes into account the sphereness of the world
        distance = (vincenty(user_geolocation, (stop_lat, stop_lon)).miles)
        stops_vincenty_diff.append(tuple([distance, stop_code]))

    user_stop = sorted(stops_vincenty_diff)

    return user_stop[0][1]


user_trip = gets_user_itinerary(agency, route, direction, destination, user_inital_stop_code)

def gets_user_itinerary(agency, route, direction, destination, user_inital_stop_code):
    """returns a list of the user's stops from inital to destination"""
    


#############################################################


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
