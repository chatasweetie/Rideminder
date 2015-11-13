from celery.task import task
from geopy.distance import vincenty
from process_data import gets_geolocation_of_a_vehicle
from twilio_process import send_text_message
from model import connect_to_db, list_of_queue_to_process

WALK_RADIUS = .20


@task()
def process_transit_request():
	"""Checks the transit_request database for request to be process and checks if vehicle geolocation 
	is within WALK_RADIUS thresold of users destination_geolocation"""
	print "got into the thing!"
	
	in_query = list_of_queue_to_process()
	print "in the queue is: ", in_query

	for request_id, vehicle_id, destination_lat, destination_lon in in_query:
		print "in the for loop working on this vehcile", vehicle_id
		print "request_id ", request_id
		vehicle_geolocation = gets_geolocation_of_a_vehicle(vehicle_id)
		destination_geolocation = (destination_lat, destination_lon)
		distance = (vincenty(destination_geolocation, vehicle_geolocation).miles)

		if distance <= WALK_RADIUS:
			print "All done"
			# send alert!
			send_text_message(user_phone)
			#is_finished to True
			request_id.complete