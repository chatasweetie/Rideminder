"""Transit Alert"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

import twilio.twiml

import process_data
import model


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
	user_phone_num = request.form.get("phone")
	line = request.form.get("line")
	bound = request.form.get("bound")
	destination_geo_location = request.form.get("destination_geo_location")
	user_geolocation = request.form.get("user_geolocation")


	vehicle_id = processes_line_and_bound_selects_closest_vehicle(line, bound)

	adds_to_queue(user_fname, user_lname, user_email, user_phone_num, destination_geo_location, message_type, vehicle_id)

	return render_template("/thank_you.html")


@app.route("/send_message", methods=['GET', 'POST'])
def send_message():
    """Respond and greet the caller by name."""
 
    from_number = request.values.get('From', None)
    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        message = "Monkey, thanks for the message!"
 
    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
