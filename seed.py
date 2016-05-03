import requests
from xml.etree import ElementTree
import os
from bart_info import gets_lat_lon_for_many_stops
from muni_info import gets_stop_lat_lon_routes

TOKEN_511 = os.environ.get("TOKEN")

wanted_agencies = ("BART", "SF-MUNI", "Caltrain")

def gets_agencies():
    """gets all the available agencies with HasDirection"""

    list_of_agencies = 'http://services.my511.org/Transit2.0/GetAgencies.aspx?token=' + TOKEN_511

    response_agencies = requests.get(list_of_agencies)

    agencies_tree = ElementTree.fromstring(response_agencies.text)

    agencies = {}

    for node in agencies_tree.iter('Agency'):
        name = node.attrib.get('Name')
        if name in wanted_agencies:
            has_direction = node.attrib.get('HasDirection')
            agencies[name] = has_direction

            # agency = Agency(
            #             name=name,
            #             has_direction=has_direction,
            #             )

            # db.session.add(agency)

    # db.session.commit()

    return agencies




    agencies_info = gets_agencies()