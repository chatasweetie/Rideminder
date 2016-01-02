from celery.task import task
from geopy.distance import vincenty
from process_data import gets_geolocation_of_a_vehicle
from twilio_process import send_text_message_walk, send_text_message_time
from model import connect_to_db, list_of_is_finished_to_process, list_of_is_finished_to_process, records_request_complete_db
from server import app, celery
from firebase import firebase
import os
from server import app


transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

WALK_RADIUS = .25
TIME_RADIUS = 3

app.debug = True
connect_to_db(app)



@celery.task()
def process_transit_request():
	"""Checks the transit_request database for request to be process and checks if vehicle geolocation 
	is within WALK_RADIUS thresold of users destination_geolocation"""

	request_to_process = list_of_is_finished_to_process()

	for request in request_to_process:
		vehicle_geolocation = gets_geolocation_of_a_vehicle(request.vehicle_id)
		destination_geolocation = (request.destination_lat, request.destination_lon)
		distance = (vincenty(destination_geolocation, vehicle_geolocation).miles)
		print "the vehicle ", request.vehicle_id
		print "the distance ", distance
		if distance <= WALK_RADIUS:
			# send alert!
			print "within walking radius"
			send_text_message_walk(request.user_phone)
			#is_finished to True
			records_request_complete_db(request)

		now = datetime.datetime.now()
		min_difference = now.minute - request.end_time.minute
		if request.end_time.hour == now.hour & min_difference <= TIME_RADIUS:
			# send alert!
			print "within time radius"
			send_text_message_time(request.user_phone)
			#is_finished to True
			records_request_complete_db(request)

