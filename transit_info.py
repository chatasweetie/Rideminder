import requests
from xml.etree import ElementTree
import os

BART_TOKEN = os.environ.get("BART_TOKEN")
# muni_stops = ['8AX-Bayshore A Express', 'Parkmerced', '30X-Marina Express', '39-Coit', '18-46th Avenue', 'T-Owl', 'Treasure Island', '1BX-California B Express', '66-Quintara', '8BX-Bayshore B Express', 'Powell Hyde Cable Car', 'Mission Rapid', 'Powell Mason Cable Car', '27-Bryant', '91-Owl', '3-Jackson', '38BX-Geary B Express', '41-Union', 'NX-N Express', '6-Haight-Parnassus', 'L-Owl', 'K-Owl', '1-California', 'J-Church', 'M-Owl', '22-Fillmore', '19th Avenue Rapid', '33-Ashbury-18th', '55-16th Street', '88-Bart Shuttle', '81X-Caltrain Express', '14-Mission', '83X-Caltrain', '14X-Mission Express', '45-Union Stockton', '28-19th Avenue', 'San Bruno Rapid', 'Fulton Rapid', '31-Balboa', '49-Van Ness Mission', '23-Monterey', '67-Bernal Heights', '38-Geary', '82X-Levi Plaza Express', '10-Townsend', '56-Rutland', 'L-Taraval', '37-Corbett', '19-Polk', '38AX-Geary A Express', '43-Masonic', '1AX-California A Express', '90-San Bruno Owl', 'Geary Rapid', '29-Sunset', '36-Teresita', '54-Felton', '47-Van Ness', '5-Fulton', 'HaightNoriega Rapid', '31AX-Balboa A Express', 'M-Ocean View', '12-Folsom Pacific', '52-Excelsior', 'N-Judah', 'KT-Ingleside Third Street', '21-Hayes', 'HaightNoriega', '48-Quintara 24th Street', 'N-Owl', '8-Bayshore', '31BX-Balboa B Express', 'California Cable Car', 'Noriega Express', '76X-Marin Headlands Express', '35-Eureka', 'F-Market And Wharves', '24-Divisadero', '9-San Bruno', '30-Stockton', '2-Clement', '44-OShaughnessy']

# made manually to connect 511 API data to BART API data
BART_ROUTES = {'Daly City - Dublin/Pleasanton': {'route_id': ['920']}, 'Daly City - Fremont': {'route_id': ['917']}, 'Millbrae/SFIA - Pittsburg/Bay Point': {'route_id': ['1027', '1735', '908']}, 'Pittsburg/Bay Point - SFIA/Millbrae': {'route_id': ['747', '722', '1561']}, 'Millbrae/Daly City - Richmond': {'route_id': ['747', '237']}, 'Dublin/Pleasanton - Daly City': {'route_id': ['747']}, 'Fremont - Daly City': {'route_id': ['747']}, 'Fremont - Richmond': {'route_id': ['237']}, 'Richmond - Daly City/Millbrae': {'route_id': ['747']}, 'Richmond - Fremont': {'route_id': ['237', '764']}, "Coliseum - Oakland Int'l Airport": {'route_id': ['']}, "Oakland Int'l Airport - Coliseum": {'route_id': ['']}}

bart_station_abbr_name = {'Ashby (Berkeley)': 'ashb', 'Powell St. (SF)': 'powl', 'Coliseum/Oakland Airport': 'cols', 'San Leandro': 'sanl', 'North Concord/Martinez': 'ncon', 'Richmond': 'rich', 'Pleasant Hill/Contra Costa Centre': 'phil', '19th St. Oakland': '19th', 'Hayward': 'hayw', '12th St. Oakland City Center': '12th', 'Bayfair (San Leandro)': 'bayf', 'Civic Center (SF)': 'civc', 'Castro Valley': 'cast', 'Fremont': 'frmt', 'Lake Merritt (Oakland)': 'lake', 'West Oakland': 'woak', '24th St. Mission (SF)': '24th', 'El Cerrito Plaza': 'plza', 'Millbrae': 'mlbr', 'Colma': 'colm', 'Downtown Berkeley': 'dbrk', 'Balboa Park (SF)': 'balb', 'Embarcadero (SF)': 'embr', 'El Cerrito Del Norte': 'deln', 'Dublin/Pleasanton': 'dubl', 'Lafayette': 'lafy', "Oakland Int'l Airport": 'oakl', 'Fruitvale (Oakland)': 'ftvl', '16th St. Mission (SF)': '16th', 'Walnut Creek': 'wcrk', 'MacArthur (Oakland)': 'mcar', 'San Bruno': 'sbrn', 'Rockridge (Oakland)': 'rock', 'Daly City': 'daly', 'Concord': 'conc', 'Pittsburg/Bay Point': 'pitt', 'Union City': 'ucty', 'Glen Park (SF)': 'glen', "San Francisco Int'l Airport": 'sfia', 'Orinda': 'orin', 'West Dublin': 'wdub', 'Montgomery St. (SF)': 'mont', 'South Hayward': 'shay', 'South San Francisco': 'ssan', 'North Berkeley': 'nbrk'}

reversed_bart_station_abbr_name = {'orin': 'Orinda', 'ftvl': 'Fruitvale (Oakland)', 'civc': 'Civic Center (SF)', 'nbrk': 'North Berkeley', 'cols': 'Coliseum/Oakland Airport', 'wcrk': 'Walnut Creek', 'woak': 'West Oakland', 'conc': 'Concord', 'ncon': 'North Concord/Martinez', 'sfia': "San Francisco Int'l Airport", 'wdub': 'West Dublin', 'embr': 'Embarcadero (SF)', 'mlbr': 'Millbrae', 'glen': 'Glen Park (SF)', 'oakl': "Oakland Int'l Airport", 'bayf': 'Bayfair (San Leandro)', 'dbrk': 'Downtown Berkeley', 'shay': 'South Hayward', 'lake': 'Lake Merritt (Oakland)', '19th': '19th St. Oakland', 'rich': 'Richmond', 'frmt': 'Fremont', 'ssan': 'South San Francisco', 'balb': 'Balboa Park (SF)', 'deln': 'El Cerrito Del Norte', 'mcar': 'MacArthur (Oakland)', 'dubl': 'Dublin/Pleasanton', '24th': '24th St. Mission (SF)', 'plza': 'El Cerrito Plaza', 'daly': 'Daly City', 'sbrn': 'San Bruno', 'hayw': 'Hayward', 'lafy': 'Lafayette', '12th': '12th St. Oakland City Center', 'phil': 'Pleasant Hill/Contra Costa Centre', 'pitt': 'Pittsburg/Bay Point', 'ashb': 'Ashby (Berkeley)', 'ucty': 'Union City', 'cast': 'Castro Valley', 'mont': 'Montgomery St. (SF)', 'colm': 'Colma', 'powl': 'Powell St. (SF)', 'rock': 'Rockridge (Oakland)', 'sanl': 'San Leandro', '16th': '16th St. Mission (SF)'}


def gets_stop_lat_lon_routes(muni_routes):
    """with a list of muni routes, parses it out and gets all the stops and their lats and lons

    returns {stop_id: {'lat': lat, 'lon': lon, 'name': name}

    """
    routes = []

    for route in muni_routes:
        i = route.split('-')
        if len(i) == 1:
            i[0].split(" ")
        routes.append(i)

    route_stops = {}

    for i in range(len(muni_routes)):

        route = routes[i]

        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r=' + route[0]

        response_agencies = requests.get(url)

        agencies_tree = ElementTree.fromstring(response_agencies.text)

        for node in agencies_tree.iter('stop'):
            stop_id = node.attrib.get('tag')
            name = node.attrib.get('title')
            lat = node.attrib.get('lat')
            lon = node.attrib.get('lon')

            if name is None:
                break

            # format to the 511 api name
            name = name.replace('&', 'and')
            # gets all the info in a beutiful dict with list of dicts
            route_stops[name] = {'stop_id': stop_id, 'lat': lat, 'lon': lon}

    return route_stops


def gets_set_of_muni_stops(route_stops):
    """returns unique stops with their name, lat and lon"""
    unique_muni_stops_lat_lon = {}

    for stop in route_stops:
        # for i in route_stops[item]:
        # import pdb; pdb.set_trace()
        unique_muni_stops_lat_lon[stop] = {'stop_id': route_stops[stop]['stop_id'], 'lat': route_stops[stop]['lat'], 'lon': route_stops[stop]['lon']}

    return unique_muni_stops_lat_lon

def gets_routes_for_bart():
    """returns all the routes for bart"""

    url = 'http://api.bart.gov/api/route.aspx?cmd=routes&key=' + BART_TOKEN

    response_agencies = requests.get(url)

    bart_tree = ElementTree.fromstring(response_agencies.text)

    stop_list = []

    for node in bart_tree.iter('station'):
        stop_list.append(node.text)

    return stop


def gets_lat_lon_for_bart_stop(stop_name):
    """returns the lat and lon for a bart stop"""

    bart_station = bart_station_abbr_name[stop_name]

    if bart_station is None:
            split_stop_name = stop_name[0].split("/")
            bart_station = bart_station_abbr_name.get(split_stop_name[0])

    url = 'http://api.bart.gov/api/stn.aspx?cmd=stninfo&orig=' + bart_station + '&key=' + BART_TOKEN

    response_agencies = requests.get(url)

    agencies_tree = ElementTree.fromstring(response_agencies.text)

    for node in agencies_tree.iter('gtfs_latitude'):
        lat = node.text

    for node in agencies_tree.iter('gtfs_longitude'):
        lon = node.text

    return (lat, lon)


def gets_caltrain_stop_lat_lon(cal_file):
    """gets the stops, lat and lon for Caltrain"""

    cal_train_stops_lat_lon = {}

    for i, row in enumerate(open(cal_file)):
            row = row.rstrip()
            stop_id, stop_code, stop_name, stop_lat, stop_lon, _, _, _, _, _, _ = row.split(",")
            # format name to match 511 format
            stop_name += " Station"

            cal_train_stops_lat_lon[stop_id] = {"stop_code": stop_code, "stop_name": stop_name, "lat": stop_lat, "lon": stop_lon}

    return cal_train_stops_lat_lon


def get_BART_routes_and_stops():
    url = 'http://api.bart.gov/api/route.aspx?cmd=routes&key=' + BART_TOKEN

    response_agencies = requests.get(url)

    bart_tree = ElementTree.fromstring(response_agencies.text)

    name = []
    abbr = []
    id = []
    num = []

    for node in bart_tree.iter('route'):
        for n in node.iter('name'):
            name.append(n.text)
        for n in node.iter('abbr'):
            abbr.append(n.text)
        for n in node.iter('routeID'):
            id.append(n.text)
        for n in node.iter('number'):
            num.append(n.text)

    routes = {}

    for i in range(len(name)):
        routes[name[i]] = {'bart_abbr': abbr[i], 'bart_id': id[i], 'bart_num': num[i], 'route_id(s)': BART_ROUTES[name[i]]['route_id']}

    routes_stops = get_stop_abb_list_for_routes_BART(routes)

    complete_route_stops = gets_bart_name_stops(routes_stops)

    del complete_route_stops["Oakland Int'l Airport - Coliseum"]
    del complete_route_stops["Coliseum - Oakland Int'l Airport"]

    return complete_route_stops

def get_stop_abb_list_for_routes_BART(routes):

    for route in routes:
        url = 'http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=' + routes[route]['bart_num'] + ' &key=' + BART_TOKEN

        response_agencies = requests.get(url)

        route_tree = ElementTree.fromstring(response_agencies.text)

        for node in route_tree.iter('station'):
            routes[route].setdefault('stop_abbr_list', []).append(node.text)

    return routes

def gets_bart_name_stops(routes):

    for route in routes:
            for stop in routes[route]['stop_abbr_list']:
                routes[route].setdefault('stop_name_list', []).append(reversed_bart_station_abbr_name[stop.lower()])

    return routes

def separates_bartroutes_and_routes(routes_511):
    """ """
    bart_511_routes = {}

    for route in routes_511:
        if routes_511[route]['agency'] == 'BART':
            bart_511_routes[routes_511[route]['route_code']] = routes_511[route]

    for route in bart_511_routes:
        try: 
            del routes_511[route]
        except KeyError:
            pass

    return bart_511_routes, routes_511

def iterable_flatter(lst): 
    """flattens out list of iterable"""

    return list(sum(lst, ()))


def gets_set_of_muni_stop_ids(lst):

    stops = list(set(lst))

    stop_ids = []

    for stop in stops:
        if stop.isdigit():
            stop_ids.append(stop)

    return stop_ids

def gets_bartroutes_and_routes(routes_511):

    bart_511_routes, routes_511 = separates_bartroutes_and_routes(routes_511)

    bart_route_stop = get_BART_routes_and_stops()

    for route in bart_route_stop:
        for route_id in bart_route_stop[route]['route_id(s)']:
            bart_route_stop[route]['direction'] = bart_511_routes[route_id].get('direction')
            bart_route_stop[route]['agency_code'] = bart_511_routes[route_id].get('agency_code')
            bart_route_stop[route]['agency'] = bart_511_routes[route_id].get('agency')
            bart_route_stop[route].setdefault('511_stop', []).extend(bart_511_routes[route_id].get('stops'))

    for route in bart_route_stop:
            bart_route_stop[route]['511_stop_ids'] = gets_set_of_muni_stop_ids(iterable_flatter(bart_route_stop[route]['511_stop']))
            del bart_route_stop[route]['511_stop']

    all_routes = dict(routes_511.items() + bart_route_stop.items())

    return all_routes
