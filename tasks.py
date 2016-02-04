# Celery task to be processed request every mintue

from celery.task import task
from geopy.distance import vincenty
from process_data import gets_geolocation_of_a_vehicle, selects_closest_vehicle
from twilio_process import send_text_message_walk, send_text_message_time
from model import connect_to_db, list_of_is_finished_to_process, list_of_is_finished_to_process, records_request_complete_db, records_request_vehicle_id_db, records_time_and_distance
from server import app, celery, sms
from firebase import firebase
import os
from server import app
import datetime


transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com/", None)

WALK_RADIUS = .25
TIME_RADIUS = 4

app.debug = True
connect_to_db(app)




@celery.task()
def process_transit_request():
	"""Gets requests from database to be process and checks if Walk Radius or Time Radius 
	are satified, then sends the text and records the transation"""

	#from the database, gets all the request that need to be processed
	request_to_process = list_of_is_finished_to_process()	

	for request in request_to_process:
		print request.vehicle_id

		#the first time the request is processed, it'll verifiy and set the closest vehicle id
		if request.vehicle_id is None:
			print "Getting vehicle id if statsment"
			vehicle_id = selects_closest_vehicle(request.vehicle_1, request.vehicle_1_distance, 
				request.vehicle_2, request.vehicle_2_distance, request.user_lat, request.user_lon)
			print "request.vehicle_1_distance:", request.vehicle_1_distance
			print "this is the closest vehicle:", vehicle_id
			records_request_vehicle_id_db(request, vehicle_id)
			print vehicle_id

		vehicle_geolocation = gets_geolocation_of_a_vehicle(request.vehicle_id)
		destination_geolocation = (request.destination_lat, request.destination_lon)
		distance = (vincenty(destination_geolocation, vehicle_geolocation).miles)
		print "the vehicle ", request.vehicle_id
		print "the distance ", distance
		
		#checks the distance of the transit vehicle	
		if distance <= WALK_RADIUS:
			# send alert!
			print "within walking radius"
			send_text_message_walk(request.user_phone)
			#is_finished to True
			records_request_complete_db(request)

		now = datetime.datetime.utcnow()
		min_difference = request.arrival_time.minute - now.minute
		print "this is the saved datetime: ", request.arrival_time
		print "this is the now: ",now
		print "this is the difference: ", min_difference 
		# to take care of the difference between a start time that is late in the hour
		# and an end time in the begining of an hour
		
		#checks the estimated arrival time	
		if min_difference > 0:
			if min_difference <= TIME_RADIUS:
				# send alert!
				print "within time radius"
				send_text_message_time(request.user_phone)
				#is_finished to True
				records_request_complete_db(request)

		records_time_and_distance(request, distance, min_difference)
		
	