import requests
from xml.etree import ElementTree
import os
from muni_info import gets_stop_lat_lon_routes, gets_set_of_muni_stops, gets_lat_lon_for_bart_stop


TOKEN_511 = os.environ.get("TOKEN_511")
BART_TOKEN = os.environ.get("BART_TOKEN")
WANTED_AGENCIES = ("BART", "SF-MUNI", "Caltrain")


def gets_agencies():
    """gets wanted agencies with HasDirection"""

    list_of_agencies = 'http://services.my511.org/Transit2.0/GetAgencies.aspx?token=' + TOKEN_511
    response_agencies = requests.get(list_of_agencies)
    agencies_tree = ElementTree.fromstring(response_agencies.text)

    agencies = {}

    for node in agencies_tree.iter('Agency'):
        name = node.attrib.get('Name')
        if name in WANTED_AGENCIES:
            has_direction = node.attrib.get('HasDirection')
            agencies[name] = has_direction

    return agencies


def adds_agencies_to_db(agencies_info):
    """ adds agency information to database"""

    for agency_ in agencies_info:
        print agency_
    #     agency = Agency(
    #                 name=agency_,
    #                 has_direction=agencies_info[agency_],
    #                 )
    #     db.session.add(agency)

    # db.session.commit()


def gets_basic_routes_for_agency(agencies):
    """gets the routes for an agency (not including the direction(s))"""

    routes = {}

    for wanted_agency in agencies:
        agency = wanted_agency
        agency_routes = 'http://services.my511.org/Transit2.0/GetRoutesForAgency.aspx?token=' + TOKEN_511 + '&agencyName=' + agency
        response_agency_routes = requests.get(agency_routes)
        route_tree = ElementTree.fromstring(response_agency_routes.text)

        for node in route_tree.iter('Route'):
            name = node.attrib.get('Name')
            code = node.attrib.get('Code')
            routes[name] = (code, agency, agencies[wanted_agency])

    return routes


def gets_stops_for_a_route(url):
    """gets all the stops for a specific route"""
    response = requests.get(url)

    stops_tree = ElementTree.fromstring(response.text)

    stops = []

    for node in stops_tree.iter('Stop'):
        name = node.attrib.get('name')
        code = node.attrib.get('StopCode')
        stops.append((name, code))

    return stops


def gets_stops_for_routes(routes):
    """gets all the stops for a routes and their directions"""

    new_routes = {}

    for route in routes:
        route_code = routes[route][0]
        agency = routes[route][1]
        direction = routes[route][2]

        if agency == "SF-MUNI":
            for direction in ["Inbound", "Outbound"]:
                url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code + '~' + direction
                stops = gets_stops_for_a_route(url)
                new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stops": stops}

        if agency == "Caltrain":
            for direction in ["NB", "SB1", "SB2", "SB3"]:
                url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code + '~' + direction
                stops = gets_stops_for_a_route(url)
                new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stops": stops}

        elif agency == "BART":
            url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code
            stops = gets_stops_for_a_route(url)
            new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stops": stops}

    return new_routes


def adds_routes_to_db(stops_routes_agencies_info):
    """adds all routes info into db"""

    for route, direction in stops_routes_agencies_info:
        direction = stops_routes_agencies_info[route, direction]['direction']
        route_code = stops_routes_agencies_info[route, direction]['route_code']
        agency = stops_routes_agencies_info[route, direction]['agency']
        stops = stops_routes_agencies_info[route, direction]['stops']

        route = Route(
                    name=route,
                    route_code=route_code,
                    direction=direction,
                    agency_name=agency,
                    )

        db.session.add(route)

    db.session.commit()


def gets_unique_stops_from_info(stops_routes_agencies_info):
    """returns a new dic of unique stops per agency"""
    stops = {"SF-MUNI": set(), "BART": set(), "Caltrain": set()}

    for route in stops_routes_agencies_info:
        for stop in stops_routes_agencies_info[route]['stops']:
            agency = stops_routes_agencies_info[route]['agency']
            stops[agency].add(stop)

    return stops


def gets_lat_lon_for_a_stop(agency, name, stop_code):
    """gets the lat and lon for a stop"""

    if agency == "SF-MUNI":
        lat = muni_stops_lat_lon[stop_code]['lat']
        lon = muni_stops_lat_lon[stop_code]['lon']

    if agency == "BART":
        lat, lon = gets_lat_lon_for_bart_stop(name)
        print lat
        print lon

    else:
        lat = 0
        lon = 0

    return (lat, lon)


def get_lats_lon_for_stops(unique_stops):
    """gets the lat and lon for unique stops"""

    unique_stops_lat_lon = {}

    for agency in unique_stops:
        for stop in unique_stops[agency]:
            name = stop[0]
            stop_code = stop[1]
            lat, lon = gets_lat_lon_for_a_stop(agency, name, stop_code)
            unique_stops_lat_lon[agency] = {'name': name, 'stop_code': stop_code, 'lat': lat, 'lon': lat}

    return unique_stops_lat_lon


def adds_stops_to_db(unique_stops):
    """all all unique stops to db"""

    for agency in unique_stops:
        for route in unique_stops[agency]:
            name = route[0]
            stop_code = route[1]
        stop = Stop(
                    stop=stop_code,
                    name=name,
                    )


#Gets agency information
agencies_info = gets_agencies()

# adds_agencies_to_db(agencies_info)

# gets the basic information for the agency routes
basic_routes_agencies_info = gets_basic_routes_for_agency(agencies_info)

# gets the stops for routes, taking into account direction
stops_routes_agencies_info = gets_stops_for_routes(basic_routes_agencies_info)

# adds_routes_to_db(stops_routes_agencies_info)

# gets the unique stops for each agency
unique_stops = gets_unique_stops_from_info(stops_routes_agencies_info)

# gets the lat and lons for SF-MUNI stops
muni_stops_lat_lon = gets_set_of_muni_stops(gets_stop_lat_lon_routes(basic_routes_agencies_info))


unique_stops_lat_lon = get_lats_lon_for_stops(unique_stops)

# stops_routes_agencies_info_muni = gets_lat_lon_for_muni_stops(stops_routes_agencies_info)

# adds_stops_to_db(unique_stops)

