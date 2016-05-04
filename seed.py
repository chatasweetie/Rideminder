import requests
from xml.etree import ElementTree
import os


TOKEN_511 = os.environ.get("TOKEN")

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

    for item in stops_routes_agencies_info:
        for stop in stops_routes_agencies_info[item]['stops']:
            agency = stops_routes_agencies_info[item]['agency']
            stops[agency].add(stop)

    return stops





agencies_info = gets_agencies()
# adds_agencies_to_db(agencies_info)
basic_routes_agencies_info = gets_basic_routes_for_agency(agencies_info)
stops_routes_agencies_info = gets_stops_for_routes(basic_routes_agencies_info)
# adds_routes_to_db(stops_routes_agencies_info)
unique_stops = gets_unique_stops_from_info(stops_routes_agencies_info)
