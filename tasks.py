# Celery task to be processed request every mintue

from process_data import gets_stop_times_by_stop, gets_user_itinerary
from twilio_process import send_text_message
from model import connect_to_db, list_of_is_finished_to_process, records_request_complete_db, update_request
from server import app, celery
import datetime

app.debug = True
connect_to_db(app)

TIME_RADIUS = 3

@celery.task()
def process_transit_request():
    """Gets requests from database to be process and checks if Time Radius
    is satified, then sends the text and records the transation"""

    #from the database, gets all the request that need to be processed
    request_to_process = list_of_is_finished_to_process()

    for request in request_to_process:
        print 'checking this request', request
        print 'current_stop:', request.current_stop

        print request.agency
        print request.route_code
        print request.destination_stop_code
        print request.inital_stop_code

        if not request.user_itinerary:
            user_itinerary = gets_user_itinerary(request.agency, request.route_code,
                                                    request.destination_stop_code,
                                                    request.inital_stop_code)

        departures_times = gets_stop_times_by_stop(request.current_stop)

        print "DepartureTime:", departures_times

        print "Route_code:", request.route_code

        if ',' in str(request.route_code):
            route_codes = str(request.route_code).split(',')
            for code in route_codes:
                routes_time = departures_times.get(code)
                if routes_time:
                    break
        else:
            routes_time = departures_times.get(request.route_code)

        print "ROUTE_TIME:", routes_time

        if not routes_time:
            continue

        if int(routes_time[0]) < 3:
            if request.current_stop == request.destination_stop_code:
                send_text_message(request.user.user_phone)
                records_request_complete_db(request)
                break

            user_itinerary = request.user_itinerary.split(', ')

            for i in range(len(user_itinerary)):
                if user_itinerary[i] == request.current_stop:
                    request.current_stop = str(user_itinerary[i + 1])
                    print 'changed current stop', request.current_stop
                    break
        # checking google estimated time
        now = datetime.datetime.utcnow()
        min_difference = request.arrival_time.minute - now.minute
        print "this is the time difference: ", min_difference

        request.time_difference = min_difference
        # to take care of the difference between a start time that is late in the hour
        # and an end time in the begining of an hour

        #checks the estimated arrival time
        if min_difference > 0:
            if min_difference <= TIME_RADIUS:
                # send alert!
                print "within time radius"
                send_text_message(request.user.user_phone)
                #is_finished to True
                records_request_complete_db(request)

        update_request(request)
