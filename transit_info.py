import requests
from xml.etree import ElementTree
import os

BART_TOKEN = os.environ.get("BART_TOKEN")
# muni_stops = ['8AX-Bayshore A Express', 'Parkmerced', '30X-Marina Express', '39-Coit', '18-46th Avenue', 'T-Owl', 'Treasure Island', '1BX-California B Express', '66-Quintara', '8BX-Bayshore B Express', 'Powell Hyde Cable Car', 'Mission Rapid', 'Powell Mason Cable Car', '27-Bryant', '91-Owl', '3-Jackson', '38BX-Geary B Express', '41-Union', 'NX-N Express', '6-Haight-Parnassus', 'L-Owl', 'K-Owl', '1-California', 'J-Church', 'M-Owl', '22-Fillmore', '19th Avenue Rapid', '33-Ashbury-18th', '55-16th Street', '88-Bart Shuttle', '81X-Caltrain Express', '14-Mission', '83X-Caltrain', '14X-Mission Express', '45-Union Stockton', '28-19th Avenue', 'San Bruno Rapid', 'Fulton Rapid', '31-Balboa', '49-Van Ness Mission', '23-Monterey', '67-Bernal Heights', '38-Geary', '82X-Levi Plaza Express', '10-Townsend', '56-Rutland', 'L-Taraval', '37-Corbett', '19-Polk', '38AX-Geary A Express', '43-Masonic', '1AX-California A Express', '90-San Bruno Owl', 'Geary Rapid', '29-Sunset', '36-Teresita', '54-Felton', '47-Van Ness', '5-Fulton', 'HaightNoriega Rapid', '31AX-Balboa A Express', 'M-Ocean View', '12-Folsom Pacific', '52-Excelsior', 'N-Judah', 'KT-Ingleside Third Street', '21-Hayes', 'HaightNoriega', '48-Quintara 24th Street', 'N-Owl', '8-Bayshore', '31BX-Balboa B Express', 'California Cable Car', 'Noriega Express', '76X-Marin Headlands Express', '35-Eureka', 'F-Market And Wharves', '24-Divisadero', '9-San Bruno', '30-Stockton', '2-Clement', '44-OShaughnessy']

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


def gets_lat_lon_for_bart_stop(stop_name):

    bart_station_abbr_name = {'Ashby (Berkeley)': 'ashb', 'Powell St. (SF)': 'powl', 'Coliseum/Oakland Airport': 'cols', 'San Leandro': 'sanl', 'North Concord/Martinez': 'ncon', 'Richmond': 'rich', 'Pleasant Hill/Contra Costa Centre': 'phil', '19th St. Oakland': '19th', 'Hayward': 'hayw', '12th St. Oakland City Center': '12th', 'Bayfair (San Leandro)': 'bayf', 'Civic Center (SF)': 'civc', 'Castro Valley': 'cast', 'Fremont': 'frmt', 'Lake Merritt (Oakland)': 'lake', 'West Oakland': 'woak', '24th St. Mission (SF)': '24th', 'El Cerrito Plaza': 'plza', 'Millbrae': 'mlbr', 'Colma': 'colm', 'Downtown Berkeley': 'dbrk', 'Balboa Park (SF)': 'balb', 'Embarcadero (SF)': 'embr', 'El Cerrito Del Norte': 'deln', 'Dublin/Pleasanton': 'dubl', 'Lafayette': 'lafy', "Oakland Int'l Airport": 'oakl', 'Fruitvale (Oakland)': 'ftvl', '16th St. Mission (SF)': '16th', 'Walnut Creek': 'wcrk', 'MacArthur (Oakland)': 'mcar', 'San Bruno': 'sbrn', 'Rockridge (Oakland)': 'rock', 'Daly City': 'daly', 'Concord': 'conc', 'Pittsburg/Bay Point': 'pitt', 'Union City': 'ucty', 'Glen Park (SF)': 'glen', "San Francisco Int'l Airport": 'sfia', 'Orinda': 'orin', 'West Dublin': 'wdub', 'Montgomery St. (SF)': 'mont', 'South Hayward': 'shay', 'South San Francisco': 'ssan', 'North Berkeley': 'nbrk'}

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
