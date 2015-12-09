"""Transit Alert"""
import os
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

import twilio.twiml

from time import sleep

from process_data import gets_a_list_of_available_line, processes_line_and_bound_selects_closest_vehicle, convert_to_e164
from model import adds_to_queue, connect_to_db

# from celery import Celery

from twilio_process import send_text_message


app = Flask(__name__)

# Required t,l.o use Flask sessions and the debug toolbar
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")

# Make Jinja2 to raise an error instead of failing sliently 
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
	user_lat = request.form.get("lat")
	user_lon = request.form.get("lng")

	destination_lat, destination_lon = destination.split(",")

	print user_lat
	print user_lon

	vehicle_id = processes_line_and_bound_selects_closest_vehicle(line, bound, destination_lat, destination_lon, user_lat, user_lon)
	print "vehicle_id is: ", vehicle_id

	user_phone = convert_to_e164(raw_user_phone_num)
	print "this is the phone number after twilioness", user_phone

	adds_to_queue(user_fname, user_lname, user_email, user_phone, vehicle_id, destination_lat, destination_lon)

	# send_text_message(user_phone)

	return render_template("/thank_you.html", user_fname=user_fname, user_phone=user_phone)

@app.route("/error")
def error():
	"""error page"""
	raise Exception("Error!")


# Celery is an open source asynchronous task queue/job queue based on distributed message passing. 
# It is focused on real-time operation, but supports scheduling as well.
# celery = Celery(app)

# celery.config_from_object('celeryconfig')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False


    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
