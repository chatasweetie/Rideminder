"""Transit Alert"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

import twilio.twiml

from time import sleep

from process_data import gets_a_list_of_available_line, processes_line_and_bound_selects_closest_vehicle, convert_to_e164
from model import adds_to_queue, connect_to_db

from celery import Celery



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

	adds_to_queue(user_fname, user_lname, user_email, user_phone, destination_lat, destination_lon, vehicle_id)

	return render_template("/thank_you.html", user_fname=user_fname, user_phone=user_phone)


# Celery is an open source asynchronous task queue/job queue based on distributed message passing. 
# It is focused on real-time operation, but supports scheduling as well.
celery = Celery(app)

celery.config_from_object('celeryconfig')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)
    
    DebugToolbarExtension(app)
    
    app.run()
