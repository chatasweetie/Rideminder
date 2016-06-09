import requests
from xml.etree import ElementTree
import os
from transit_info import gets_stop_lat_lon_routes, gets_set_of_muni_stops, gets_lat_lon_for_bart_stop, gets_caltrain_stop_lat_lon, gets_bartroutes_and_routes
from model import db, connect_to_db, Agency, Route, Stop, Route_Stop
from server import app


TOKEN_511 = os.environ.get("TOKEN_511")
BART_TOKEN = os.environ.get("BART_TOKEN")
WANTED_AGENCIES = ("BART", "SF-MUNI", "Caltrain")

if __name__ == '__main__':
    import os

    os.system("dropdb ridemindertest")
    print "dropdb"
    os.system("createdb ridemindertest")
    print "createdb"

    connect_to_db(app)
    print "connect to db"

    # Make the tables
    db.create_all()
    print "create tables"


def gets_agencies():
    """gets wanted agencies and HasDirection

    example: {Agency: has_direction}
    """
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

        agency = Agency(
                    name=str(agency_),
                    has_direction=agencies_info[agency_],
                    )
        db.session.add(agency)

    db.session.commit()
    print "Agencies Added to DB"


def gets_basic_routes_for_agency(agencies):
    """gets the routes for an agency (not including the direction(s))

    example: {Route_name = {route_code, route_agency, agency_hasdirection}
    """
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
                new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stop_list": stops, "agency_code": 3}

        if agency == "Caltrain":
            for direction in ["NB", "SB1", "SB2", "SB3"]:
                url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code + '~' + direction
                stops = gets_stops_for_a_route(url)
                new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stop_list": stops, "agency_code": 1}

        elif agency == "BART":
            url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code
            stops = gets_stops_for_a_route(url)
            new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stop_list": stops, "agency_code": 2}

    return new_routes


def adds_routes_to_db(stops_routes_agencies_info):
    """adds all routes info into db"""

    for route in stops_routes_agencies_info:
        direction = stops_routes_agencies_info[route]['direction']
        route_code = stops_routes_agencies_info[route]['route_code']
        stop_list = stops_routes_agencies_info[route]['stop_list']
        agency_code = stops_routes_agencies_info[route]['agency_code']

        route = Route(
                    name=str(route),
                    route_code=str(route_code),
                    direction=str(direction),
                    stop_list=str(stop_list),
                    agency_id=agency_code,
                    )

        db.session.add(route)

    db.session.commit()

    print "Routes Added to DB"


def gets_unique_stops_from_info(stops_routes_agencies_info):
    """returns a new dic of unique stops per agency"""

    stops = {"SF-MUNI": set(), "BART": set(), "Caltrain": set()}

    for route in stops_routes_agencies_info:
        for stop in stops_routes_agencies_info[route]['stop_list']:
            agency = stops_routes_agencies_info[route]['agency']
            stops[agency].add(stop)

    return stops


def gets_lat_lon_for_a_stop(agency, name, stop_code):
    """gets the lat and lon for a stop"""

    if agency == "SF-MUNI":
        stop_info = muni_stops_lat_lon.get(name)

        if stop_info:
            lat = stop_info['lat']
            lon = stop_info['lon']
        else:
            lat = "******"
            lon = 0

    if agency == "BART":
        lat, lon = gets_lat_lon_for_bart_stop(name)

    if agency == "Caltrain":
        stop_info = cal_train_stops_lat_lon.get(stop_code)
        if stop_info:
            lat = stop_info['lat']
            lon = stop_info['lon']

        else:
            lat = "******"
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

            # some stops need to have stop code converted
            if lat == "******":
                stop_code_convert = '1' + stop_code
                lat, lon = gets_lat_lon_for_a_stop(agency, name, stop_code_convert)

            # catches if stop does not have a lat/lon
            if lat == "******":
                unique_stops_lat_lon[stop] = {'name': name, 'stop_code': stop_code, 'lat': 0, 'lon': 0}

            else:
                unique_stops_lat_lon[stop] = {'name': name, 'stop_code': stop_code, 'lat': lat, 'lon': lon}

    return unique_stops_lat_lon


def adds_stops_to_db(unique_stops):
    """all all unique stops to db"""

    for stop in unique_stops:
        name = stop[0]
        stop_code = stop[1]
        lat = unique_stops[stop]['lat']
        lon = unique_stops[stop]['lon']

        stop = Stop(
                    stop_code=stop_code,
                    name=str(name),
                    lat=lat,
                    lon=lon,
                    )
        db.session.add(stop)
        db.session.commit()
    print "Stops Added to DB"


def adds_routestop_to_db(stops_routes_agencies_info):
    """add the relationship between routes and stops to db"""
    for route in stops_routes_agencies_info:
        route_code = stops_routes_agencies_info[route]['route_code']

        route_db = db.session.query(Route).filter(Route.route_code == route_code).first()

        for stop in stops_routes_agencies_info[route]['stop_list']:

            stop_id = stop[1]

            stops = db.session.query(Stop).filter(Stop.stop_code == stop_id).all()
            if len(stops) > 0:

                route_stop = Route_Stop(
                                        route_id=route_db.route_id,
                                        stop_id=stop_id,
                                        )
                db.session.add(route_stop)
            else:
                print "stops", stops
                print "stop_id", stop_id

        db.session.commit()
    print "RouteStops Added to DB"


#Gets agency information
agencies_info = gets_agencies()
print "got agencies from api"

# gets the basic information for the agency routes
basic_routes_agencies_info = gets_basic_routes_for_agency(agencies_info)
print "got routes and agencies from api"

# gets the stops for routes, taking into account direction
stops_routes_agencies_info = gets_stops_for_routes(basic_routes_agencies_info)
print "got stops, routes and agencies from api"

# gets the unique stops for each agency
unique_stops = gets_unique_stops_from_info(stops_routes_agencies_info)
print "got unique stops from api"

# corrects 511 bug with BART API
stop_routes_agencies_info_bart = gets_bartroutes_and_routes(stops_routes_agencies_info)

# gets the lat and lons for SF-MUNI stops
muni_stops_lat_lon = gets_set_of_muni_stops(gets_stop_lat_lon_routes(basic_routes_agencies_info))
print "got muni stops from api"

# gets the lat and lons for Caltrain stops
cal_train_stops_lat_lon = gets_caltrain_stop_lat_lon("seed_data/stops.txt")
print "got caltrain stops from api"

# all unique stops with lat lon
unique_stops_lat_lon = get_lats_lon_for_stops(unique_stops)
print "got unique stops with lat/lon from api"


if __name__ == '__main__':
    # Adds data to db
    adds_agencies_to_db(agencies_info)
    adds_routes_to_db(stop_routes_agencies_info_bart)
    adds_stops_to_db(unique_stops_lat_lon)
    adds_routestop_to_db(stops_routes_agencies_info)
