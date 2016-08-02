"""Functions to process the data"""
from geopy.distance import vincenty
import phonenumbers
import os
import datetime
import requests
from xml.etree import ElementTree
from model import connect_to_db, gets_stop_name_db, gets_stop_db, gets_route_db, gets_route_id_db

GOOGLE_MAP_API_KEY = os.environ.get("GOOGLE_MAP_API_KEY")

TOKEN_511 = os.environ.get("TOKEN_511")

# user_name = 'jessica'
# raw_user_phone_num = '(760)2522077'
# agency = 'BART'
# route_code = '153'
# user_inital_stop = '14'
# destination_stop = '32'
# # user_lat = 
# # user_lon = 


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


def gets_stops_from_route(stop_list, agency_id):
    """reformats stop_list to be useable

        >>> stop_list = u"['Daly City', 'Balboa Park (SF)', 'Glen Park (SF)', '24th St. Mission (SF)', '16th St. Mission (SF)', 'Civic Center (SF)', 'Powell St. (SF)', 'Montgomery St. (SF)', 'Embarcadero (SF)', 'West Oakland', 'Lake Merritt (Oakland)', 'Fruitvale (Oakland)', 'Coliseum/Oakland Airport', 'San Leandro', 'Bayfair (San Leandro)', 'Castro Valley', 'West Dublin', 'Dublin/Pleasanton']"
        >>> agency_id = 3
        >>> gets_stops_from_route(stop_list, agency_id)
        [u'Daly City', u'Balboa Park (SF)', u'Glen Park (SF)', u'24th St. Mission (SF)', u'16th St. Mission (SF)', u'Civic Center (SF)', u'Powell St. (SF)', u'Montgomery St. (SF)', u'Embarcadero (SF)', u'West Oakland', u'Lake Merritt (Oakland)', u'Fruitvale (Oakland)', u'Coliseum/Oakland Airport', u'San Leandro', u'Bayfair (San Leandro)', u'Castro Valley', u'West Dublin', u'Dublin/Pleasanton']

    """

    # bart stops are handled differently
    if agency_id == 3:
        # do something else with BART
        stop_list = stop_list[2:-2]
        stop_list = stop_list.split("', '")

        return stop_list

    s = stop_list[1:-2]
    t = s.split(')')
    d = ''.join(t)
    c = d.split('(')
    e = ''.join(c)
    j = e.split("'")
    g = ''.join(j)
    h = g.split(', ')

    i =[]
    u = []
    for num in range(len(h)):
        if num % 2 == 0:
            i.append(h[num])
        else:
            u.append(h[num])

    return zip(i, u)


def parse_route_stop_for_user(route_stops, user_inital_stop_db,
                                    destination_stop_db, count=0):
    """creates an itinerary from the user's inital stop to their destination

        >>> route_stops = ['Daly City', 'Balboa Park (SF)', 'Glen Park (SF)', '24th St. Mission (SF)', '16th St. Mission (SF)', 'Civic Center (SF)', 'Powell St. (SF)', 'Montgomery St. (SF)', 'Embarcadero (SF)', 'West Oakland', 'Lake Merritt (Oakland)', 'Fruitvale (Oakland)', 'Coliseum/Oakland Airport', 'San Leandro', 'Bayfair (San Leandro)', 'Castro Valley', 'West Dublin', 'Dublin/Pleasanton']
        >>> user_inital_stop = u'14'
        >>> destination_stop = u'32'
        >>> destination_stop = gets_stop_db(destination_stop)
        >>> user_inital_stop = gets_stop_db(user_inital_stop)
        >>> itinerary = parse_route_stop_for_user(route_stops, user_inital_stop,destination_stop)
        >>> itinerary
        '14, 15, 17, 19, 38, 36, 34, 32'

    """

    start = False
    itinerary = ""

    for stop in route_stops:
        if stop == str(user_inital_stop_db.name):
            start = True
        if start:
            stop_db = gets_stop_name_db(stop)
            if stop_db == []:
                continue
            itinerary = itinerary + str(stop_db[0].stop_code) + ', '
            if stop == str(destination_stop_db.name):
                return itinerary[:-2]

    route_stops.reverse()
    if count == 1:
        return itinerary

    return parse_route_stop_for_user(route_stops, user_inital_stop_db,
                                    destination_stop_db, 1)


def gets_user_itinerary(agency, route_code, destination_stop,
                                            user_inital_stop, route_name):
    """returns a list of the user's stops from inital to destination

        >>> agency = u'BART'
        >>> route_code = u'920'
        >>> destination_stop = u'32'
        >>> user_inital_stop = u'14'
        >>> route_name = u'Daly City - Dublin/Pleasanton'
        >>> user_itinerary = gets_user_itinerary(agency, route_code, destination_stop, user_inital_stop, route_name)
        >>> user_itinerary
        '14, 15, 17, 19, 38, 36, 34, 32'

    """

    route = gets_route_id_db(route_code)
    if not route:
        route = gets_route_db(route_code)
    destination_stop = gets_stop_db(destination_stop)
    user_inital_stop = gets_stop_db(user_inital_stop)

    route_stops = gets_stops_from_route(str(route.stop_list), route.agency.agency_id)

    itinerary = parse_route_stop_for_user(route_stops, user_inital_stop,
                                                        destination_stop)

    return itinerary


def gets_user_stop_id(user_lat, user_lon, route):
    """processes the lat/lon of user to find closest stop for their route

        >>> user_lat = 37.785152
        >>> user_lon = -122.406581
        >>> from model import gets_route_id_db
        >>> route_code = '153'
        >>> route = gets_route_id_db(route_code)
        >>> gets_user_stop_id(user_lat, user_lon, route)
        14
    """

    user_geolocation = (user_lat,user_lon)
    stops_vincenty_diff = []

    for stop in route.stops:
        stop_lat = stop.lat
        stop_lon = stop.lon
        stop_code = stop.stop_code
        stop_geolocation = (stop_lat, stop_lon)
        distance = (vincenty(user_geolocation, (stop_lat, stop_lon)).miles)
        stops_vincenty_diff.append(tuple([distance, stop_code]))

    user_stop = sorted(stops_vincenty_diff)

    return user_stop[0][1]

# Estimated time
#############################################################

def process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_stop):
    """takes in geolocations and returns the arrival time as a datatime object of when the
    transit is completed

        >>> user_lat = 37.784991
        >>> user_lon = -122.406857
        destination_stop = '32'
        >>> destination_stop = gets_stop_db(destination_stop)
        >>> arrival_time_datetime = process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_stop)
        >>> type(arrival_time_datetime)
        <type 'datetime.datetime'>
    """

    destination_lat = destination_stop.lat
    destination_lon = destination_stop.lon

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


def gets_stop_times_by_stop(stop):
    """returns the time and routes of a stop

        >>> times = gets_stop_times_by_stop('32')
        >>> type(times)
        <type 'dict'>
    """

    url = 'http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=' + TOKEN_511 + '&stopcode=' + stop

    response = requests.get(url)

    departure_tree = ElementTree.fromstring(response.text)

    departures = {}

    for node in departure_tree.iter('Route'):
        code = node.attrib.get('Code')
        for n in node.iter('DepartureTime'):
            departures.setdefault(code, []).append(n.text)

    return departures


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "connected to db"
