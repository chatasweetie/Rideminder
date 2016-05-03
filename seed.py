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

            # agency = Agency(
            #             name=name,
            #             has_direction=has_direction,
            #             )

            # db.session.add(agency)

    # db.session.commit()

    return agencies


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

        #     route = Route(
        #                 route_id=int(code),
        #                 name=name,
        #                 agency_name=agency
        #                 )

        #     db.session.add(route)

        # db.session.commit()

    return routes


def gets_stops_for_a_route(url):
        response = requests.get(url)

        stops_tree = ElementTree.fromstring(response.text)

        stops = []

        for node in stops_tree.iter('Stop'):
            name = node.attrib.get('name')
            code = node.attrib.get('StopCode')
            stops.append((name, code))

        return stops


def gets_stops_for_routes(routes):
    """gets all the stops for a route"""

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


agencies_info = gets_agencies()
basic_routes_agencies_info = gets_basic_routes_for_agency(agencies_info)
stops_routes_agencies_info = gets_stops_for_routes(routes_agencies_info)
