"""To Unit test then Integration Test my Transit Alert Application"""
import unittest
from unittest import TestCase
import doctest
from process_data import convert_to_e164, process_lat_lng_get_arrival_datetime, gets_user_stop_id, gets_user_itinerary, parse_route_stop_for_user, gets_stops_from_route
from tasks import process_transit_request
import datetime
from server import app
import server
from model import db, Transit_Request, gets_stop_db, gets_route_id_db, User, adds_transit_request
from flask_sqlalchemy import SQLAlchemy
from twilio_process import send_text_message
from nose.tools import eq_ #to test Celery

# to test:
# python test.py
# coverage:
# coverage run --omit=env/* test.py
# for report:
# coverage report -m
# coverage html

mock_db = SQLAlchemy()

######################################################
def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests."""

    tests.addTests(doctest.DocTestSuite(server))
    tests.addTests(doctest.DocFileSuite("tests.txt"))
    return tests

########################################################
class UnitTestTwillioTestCase(unittest.TestCase):
    """Test Twilio code"""

    def test_convert_to_e164(self):
        self.assertEqual(convert_to_e164("(843)323-2343"), u'+18433232343')
        print "complete phone number convertion test"

    def test_convert_to_e164_empty(self):
        self.assertEqual(convert_to_e164(""), None)
        print "complete phone number convertion test"

    def test_convert_to_e164_plus_sign(self):
        self.assertEqual(convert_to_e164("+18294039493"), u'+18294039493')
        print "complete phone number convertion test"

    def test_send_text_message(self):
        self.assertEqual(send_text_message(+12025550141), None)

########################################################
class UnitTestDataProcessing(unittest.TestCase):
    """Test checking the user's lat and lon"""

    def test_gets_user_stop_id(self):
        user_lat = 37.785152
        user_lon = -122.406581
        route_code = '153'
        route = gets_route_id_db(route_code)
        self.assertEqual(gets_user_stop_id(user_lat, user_lon, route), 14)
        print "complete gets_user_stop_id"

    def test_gets_user_itinerary(self):
        agency = u'BART'
        route_code = u'920'
        destination_stop = u'32'
        user_inital_stop = u'14'
        route_name = u'Daly City - Dublin/Pleasanton'
        self.assertEqual(gets_user_itinerary(agency, route_code, destination_stop, user_inital_stop, route_name), '14, 15, 17, 19, 38, 36, 34, 32')
        print "complete gets_user_itinerary"

    def test_parse_route_stop_for_user(self):
        route_stops = ['Daly City', 'Balboa Park (SF)', 'Glen Park (SF)', '24th St. Mission (SF)', '16th St. Mission (SF)', 'Civic Center (SF)', 'Powell St. (SF)', 'Montgomery St. (SF)', 'Embarcadero (SF)', 'West Oakland', 'Lake Merritt (Oakland)', 'Fruitvale (Oakland)', 'Coliseum/Oakland Airport', 'San Leandro', 'Bayfair (San Leandro)', 'Castro Valley', 'West Dublin', 'Dublin/Pleasanton']
        user_inital_stop = u'14'
        destination_stop = u'32'
        destination_stop = gets_stop_db(destination_stop)
        user_inital_stop = gets_stop_db(user_inital_stop)
        self.assertEqual(parse_route_stop_for_user(route_stops, user_inital_stop, destination_stop), '14, 15, 17, 19, 38, 36, 34, 32')

    def test_gets_stops_from_route_bart(self):
        stop_list = u"['Daly City', 'Balboa Park (SF)', 'Glen Park (SF)', '24th St. Mission (SF)', '16th St. Mission (SF)', 'Civic Center (SF)', 'Powell St. (SF)', 'Montgomery St. (SF)', 'Embarcadero (SF)', 'West Oakland', 'Lake Merritt (Oakland)', 'Fruitvale (Oakland)', 'Coliseum/Oakland Airport', 'San Leandro', 'Bayfair (San Leandro)', 'Castro Valley', 'West Dublin', 'Dublin/Pleasanton']"
        agency_id = 3
        self.assertEqual(gets_stops_from_route(stop_list, agency_id), [u'Daly City', u'Balboa Park (SF)', u'Glen Park (SF)', u'24th St. Mission (SF)', u'16th St. Mission (SF)', u'Civic Center (SF)', u'Powell St. (SF)', u'Montgomery St. (SF)', u'Embarcadero (SF)', u'West Oakland', u'Lake Merritt (Oakland)', u'Fruitvale (Oakland)', u'Coliseum/Oakland Airport', u'San Leandro', u'Bayfair (San Leandro)', u'Castro Valley', u'West Dublin', u'Dublin/Pleasanton'])
    
    def test_gets_stops_from_route_muni(self):
        stop_list = u"[('Mission St and 13th St', '15546'), ('Mission St and 14th St', '15547'), ('Mission St and 16th St', '15551'), ('Mission St and 18th St', '15553'), ('Mission St and 20th St', '15557'), ('Mission St and 22nd St', '15561'), ('Mission St and 24th St', '15565'), ('Mission St and 26th St', '15567'), ('Mission St and 30th St', '15571'), ('Mission St and Appleton Ave', '15577'), ('Mission St and Brazil Ave', '15582'), ('Mission St and Cortland Ave', '15583'), ('Mission St and Excelsior Ave', '15586'), ('Mission St and Highland Ave', '15596'), ('Mission St and Murray St', '15605'), ('Mission St and Richland Ave', '15613'), ('Mission St and Silver Ave', '15620'), ('Mission St and Trumbull St', '15624'), ('Ocean Ave and Balboa Park Bart', '15781'), ('Ocean Ave and Cayuga Ave', '15783'), ('Ocean Ave and Howth St', '15791'), ('Ocean Ave and Otsego Ave', '15800'), ('Ocean Ave and San Jose St', '15805'), ('City College Terminal Phelan Loop', '15926'), ('S Van Ness Ave and Mission St', '16473'), ('Van Ness Ave and Broadway', '16798'), ('Van Ness Ave and Chestnut St', '16800'), ('Van Ness Ave and Clay St', '16803'), ('Van Ness Ave and Eddy St', '16804'), ('Van Ness Ave and Bay St', '16806'), ('Van Ness Ave and Jackson St', '16813'), ('Van Ness Ave and McAllister St', '16815'), ('Van Ness Ave and Market St', '16817'), ('Van Ness Ave and North Point St', '16818'), ('Van Ness Ave and No Point St', '16820'), ('Van Ness Ave and OFarrell St', '16823'), ('Van Ness Ave and Sutter St', '16829'), ('Van Ness Ave and Union St', '16833'), ('Mission St and Power St', '17841')]"
        agency_id = 1
        self.assertEqual(gets_stops_from_route(stop_list, agency_id), [(u'Mission St and 13th St', u'15546'), (u'Mission St and 14th St', u'15547'), (u'Mission St and 16th St', u'15551'), (u'Mission St and 18th St', u'15553'), (u'Mission St and 20th St', u'15557'), (u'Mission St and 22nd St', u'15561'), (u'Mission St and 24th St', u'15565'), (u'Mission St and 26th St', u'15567'), (u'Mission St and 30th St', u'15571'), (u'Mission St and Appleton Ave', u'15577'), (u'Mission St and Brazil Ave', u'15582'), (u'Mission St and Cortland Ave', u'15583'), (u'Mission St and Excelsior Ave', u'15586'), (u'Mission St and Highland Ave', u'15596'), (u'Mission St and Murray St', u'15605'), (u'Mission St and Richland Ave', u'15613'), (u'Mission St and Silver Ave', u'15620'), (u'Mission St and Trumbull St', u'15624'), (u'Ocean Ave and Balboa Park Bart', u'15781'), (u'Ocean Ave and Cayuga Ave', u'15783'), (u'Ocean Ave and Howth St', u'15791'), (u'Ocean Ave and Otsego Ave', u'15800'), (u'Ocean Ave and San Jose St', u'15805'), (u'City College Terminal Phelan Loop', u'15926'), (u'S Van Ness Ave and Mission St', u'16473'), (u'Van Ness Ave and Broadway', u'16798'), (u'Van Ness Ave and Chestnut St', u'16800'), (u'Van Ness Ave and Clay St', u'16803'), (u'Van Ness Ave and Eddy St', u'16804'), (u'Van Ness Ave and Bay St', u'16806'), (u'Van Ness Ave and Jackson St', u'16813'), (u'Van Ness Ave and McAllister St', u'16815'), (u'Van Ness Ave and Market St', u'16817'), (u'Van Ness Ave and North Point St', u'16818'), (u'Van Ness Ave and No Point St', u'16820'), (u'Van Ness Ave and OFarrell St', u'16823'), (u'Van Ness Ave and Sutter St', u'16829'), (u'Van Ness Ave and Union St', u'16833'), (u'Mission St and Power St', u'17841')])

#######################################################
# class UnitTestTransit_Request(unittest.TestCase):
#     """Testing wit Mock Data"""

#     print"got into mock data class"

#     def setUp(self):
#         """Creating mock firebase to test aganist"""

#         mock_transit_firebase = firebase.FirebaseApplication("https://popping-torch-2216.firebaseio.com/sf-muni", None)

#         self._old_transit_firebase = process_data.transit_firebase
#         process_data.transit_firebase = mock_transit_firebase

#     def tearDown(self):
#         """Resets my database"""
#         process_data.transit_firebase = self._old_transit_firebase

#     def test_gets_a_dic_of_vehicle(self):
#         print "test gets_a_dic_of_vehicle"
#         results = {u'1426': u'True', u'1410': u'True', u'1402': u'True', u'1413': u'True', u'1415': u'True', u'1404': u'True'}
#         self.assertEqual(gets_a_dic_of_vehicle("N"), results)

#     # def test_validates_bound_direction_of_vehicles_in_line(self):
#     #     dic = gets_a_dic_of_vehicle("N")
#     #     results = [u'1426', u'1410', u'1402', u'1413', u'1415']
#     #     self.assertEqual(validates_bound_direction_of_vehicles_in_line(dic, "O"), results)

#     # def test_validates_bound_direction_not_be(self):
#     #     dic = gets_a_dic_of_vehicle("N")
#     #     negative_results = "1404"
#     #     self.assertNotEqual(validates_bound_direction_of_vehicles_in_line(dic, "O"), negative_results)

#     def test_gets_geolocation_of_a_vehicle(self):
#         self.assertEqual(gets_geolocation_of_a_vehicle(1402), (37.7213, -122.46912))

#     # def test_sorts_vehicles_dic_by_distance(self):
#     #     dic = gets_a_dic_of_vehicle("N")
#     #     bound_dic = validates_bound_direction_of_vehicles_in_line(dic, "O")
#     #     results = [(0.9313235948899348, u'1426'), (4.275886490639952, u'1415'), (4.7115931592023585, u'1410'), (5.526469350242915, u'1402'), (5.59359790362578, u'1413')]
#     #     self.assertEqual(sorts_vehicles_dic_by_distance(bound_dic, 37.7846810, -122.4073680), results)

#     def test_selects_closest_vehicle(self):
#         vehicle_1 = 1426
#         vehicle_1_distance = 0.12315312469250524
#         vehicle_2 = 1438
#         vehicle_2_distance = 0.12315312469250524
#         user_lat = 37.785152
#         user_lon = -122.406581
#         self.assertEqual(selects_closest_vehicle(vehicle_1, vehicle_1_distance, vehicle_2, vehicle_2_distance, user_lat, user_lon), "1438")

#     def test_selects_closest_vehicle(self):
#         user_lat = 37.7846810
#         user_lon = -122.4073680
#         destination_lat = 37.7846810
#         destination_lon = -122.4073680
#         bound = "O"
#         line = "N"
#         results = "1426"
#         self.assertEqual(selects_closest_vehicle(line, bound, destination_lat, destination_lon, user_lat, user_lon), line)

########################################################
class UnitTestMockDataForCelery(unittest.TestCase):
    """Testing wit Mock Data"""

    print"got into mock data class for celery"

    def setUp(self):
        """Creating mock data to test aganist"""

        user_db = User.query.filter_by(user_name="Jessica").first()
        user_inital_stop = '14'
        user_inital_stop = gets_stop_db(user_inital_stop)
        destination_stop = '32'
        destination_stop = gets_stop_db(destination_stop)
        route_code = '153'
        route = gets_route_id_db(route_code)
        agency = 'BART'
        arrival_time_datetime = datetime.datetime(2016, 7, 31, 4, 39, 53, 25840)

        adds_transit_request(user_inital_stop.stop_code, destination_stop.stop_code, agency,  route.name,  route.route_code,  arrival_time_datetime, user_db)

    def tearDown(self):
        """Resets my database"""

        t_r = Transit_Request.query.all()
        for t in t_r:
            db.session.delete(t)
        db.session.commit()

    def test_process_transit_request(self):
        """test celery process"""

        rst = process_transit_request.apply().get()
        t_r = Transit_Request.query.first()
        self.assertIsNotNone(t_r.user_itinerary)

#     def test_gets_stop_times_by_stop(self):
#         """test gets_stop_times_by_stop"""

# TYPE>        self.assertEqual(gets_stop_times_by_stop('14'), [])


class UnitTestDateTime(unittest.TestCase):
    """Test Datetime Functionality"""
    print "processing datetime test"

    def test_process_lat_lng_get_arrival_datetime(self):
        user_lat = 37.784991
        user_lon = -122.406857
        destination_stop = '32'
        destination_stop = gets_stop_db(destination_stop)
        result = process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_stop)
        from datetime import datetime
        now = datetime.now()
        self.assertEqual(result.year, now.year)


class IntergrationServerTest(unittest.TestCase):
    """Integration Test: testing flask sever"""

    def setUp(self):
        print "(setUp ran)"
        self.client = server.app.test_client()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        print "completed homepage test"

    def test_user_input_form(self):
        test_client = server.app.test_client()
        result = test_client.post('/thank-you', data={'name': 'Jessica', 'phone': '13604508678',
                                                        'agency': 'BART', 'route': '153',
                                                        'user_stop': '14', 'destination_stop': '32',
                                                        'lat': '', 'lng': ''})
        self.assertIn('We have you going from Powell St. (SF) to San Leandro on the Daly City - Dublin/Pleasanton route. We will text you at +13604508678 when you are within 2 mins of your destination.', result.data)



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///examplerideminder'
    mock_db.app = app
    mock_db.init_app(app)


if __name__ == '__main__':
    unittest.main()
    from server import app
    connect_to_db(app)
    mock_db.create_all()
    print "Connected to DB."
