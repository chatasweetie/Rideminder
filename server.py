"""Transit Alert"""
import os
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

# import twilio.twiml

from process_data import gets_a_list_of_available_line, processes_line_and_bound_selects_two_closest_vehicle, convert_to_e164, process_lat_lng_get_arrival_datetime
from model import adds_to_queue, connect_to_db

from celery import Celery

from twilio_process import send_text_message_walk, send_text_message_time
import datetime

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
	user_fname = request.form.get("name")
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

	# user_lat= 37.785152
	# user_lon = -122.406581
	# destination_lat = 37.762028
	# destination_lon = -122.470790

	list_of_vincenty_vehicle = processes_line_and_bound_selects_two_closest_vehicle(line, bound, 
											destination_lat, destination_lon, user_lat, user_lon)
	vehicle_1 = list_of_vincenty_vehicle[0][1]
	vehicle_1_distance = list_of_vincenty_vehicle[0][0]
	vehicle_2 = list_of_vincenty_vehicle[1][1]
	vehicle_2_distance = list_of_vincenty_vehicle[1][0]


	user_phone = convert_to_e164(raw_user_phone_num)
	print "this is the phone number after twilioness", user_phone

	arrival_time_datetime = datetime.datetime(2016, 1, 12, 22, 05, 58, 70745)
	# arrival_time_datetime = process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_lat, 
																	# destination_lon)
	print arrival_time_datetime

	adds_to_queue(user_fname, user_email, user_phone, user_lat, user_lon, destination_lat, destination_lon, 
				   vehicle_1, vehicle_1_distance, vehicle_2, vehicle_2_distance, arrival_time_datetime)

	return render_template("/thank_you.html", user_fname=user_fname, user_phone=user_phone)


@app.route('/sms', methods=['GET', 'POST'])
def sms():
	response = twiml.Response()
	response.sms("You are within 3 blocks of your destination, thank you for using Rideminder")

	return str(response)

@app.route("/error")
def error():
	"""error page"""
	raise Exception("Error!")


# Celery is an open source asynchronous task queue/job queue based on distributed message passing. 
# It is focused on real-time operation, but supports scheduling as well.
celery = Celery(app)

celery.config_from_object('celeryconfig')


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
