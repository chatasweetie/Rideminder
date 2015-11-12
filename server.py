"""Transit Alert"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

import twilio.twiml

from time import sleep

from process_data import gets_a_list_of_available_line, processes_line_and_bound_selects_closest_vehicle, convert_to_e164, gets_geolocation_of_a_vehicle
from model import adds_to_queue, connect_to_db, list_of_queue_to_process

from celery import Celery
WALK_RADIUS = .20

from geopy.distance import vincenty

from twilio_process import send_text_message


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "123456"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def index():
    """Homepage."""
    list_of_available_lines = gets_a_list_of_available_line()

    return render_template("homepage.html", list_of_available_lines=list_of_available_lines)

@app.route("/user_input", methods=["POST"])
def process_user_info():
	"""recieves the user data and sends data to appropiate processes"""
	user_fname = request.form.get("fname")
	user_lname = request.form.get("lname")
	user_email = request.form.get("email")
	raw_user_phone_num = request.form.get("phone")
	line = str(request.form.get("line"))
	bound = str(request.form.get("bound"))
	destination = request.form.get("destination")
	# user_geolocation = request.form.get("user_geolocation")

	user_lat= 37.7846810
	user_lon = -122.4073680
	destination_lat = 37.7846810
	destination_lon = -122.4073680

	if bound == "Inbound":
		bound = "I"
	elif bound == "Outbound":
		bound = "O"

	vehicle_id = processes_line_and_bound_selects_closest_vehicle(line, bound, destination_lat, destination_lon, user_lat, user_lon)
	print "vehicle_id is: ", vehicle_id

	user_phone = convert_to_e164(raw_user_phone_num)
	print "this is the phone number after twilioness", user_phone

	send_text_message(user_phone)

	adds_to_queue(user_fname, user_lname, user_email, user_phone, destination_lat, destination_lon, vehicle_id)

	return render_template("/thank_you.html", user_fname=user_fname, user_phone=user_phone)


# Celery is an open source asynchronous task queue/job queue based on distributed message passing. 
# It is focused on real-time operation, but supports scheduling as well.
# celery = Celery(app)

# CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
# CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"

# celery.config_from_object(
# 	CELERY_BROKER_URL="amqp://guest:guest@localhost:5672//",
# 	CELERY_RESULT_BACKEND="amqp://guest:guest@localhost:5672//")


# @celery.task()
# def process_transit_request():
# 	"""Checks the transit_request database for request to be process and checks if vehicle geolocation 
# 	is within WALK_RADIUS thresold of users destination_geolocation"""
# 	in_query = list_of_queue_to_process()

# 	for request_id, vehicle_id, destination_lat, destination_lon in in_query:
# 		vehicle_geolocation = gets_geolocation_of_a_vehicle(vehicle_id)
# 		destination_geolocation = (destination_lat, destination_lon)
# 		distance = (vincenty(destination_geolocation, vehicle_geolocation).miles)

# 		if distance <= WALK_RADIUS:
# 			# send alert!
# 			print "All done"
# 			#is_finished to True
# 			request_id.complete

@app.route("/message", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    message = "To use Transit Alert, go to www.chata.com"
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)


# @app.route("/send_message", methods=['GET', 'POST'])
# def send_message():
#     """Respond and greet the caller by name."""

 
#     from_number = request.values.get('From', None)
#     if from_number in callers:
#         message = callers[from_number] + ", thanks for the message!"
#     else:
#         message = "Monkey, thanks for the message!"
 
#     resp = twilio.twiml.Response()
#     resp.message(message_with_3_blocks)
 
#     return str(resp)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)
    
    DebugToolbarExtension(app)
    
    app.run()
