"""Transit Alert"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

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
    

    return render_template("homepage.html")

@app.route("/user_input", methods=["POST"])
def process_user_info():
	"""recieves the user data and sends data to appropiate processes"""
	user_fname = request.form.get("user_fname")
	user_lname = request.form.get("user_lname")
	user_email = request.form.get("user_email")
	user_phone_num = request.form.get("user_phone_num")
	line = request.form.get("line")
	bound = request.form.get("bound")
	destination_geo_location = request.form.get("destination_geo_location")
	user_geolocation = request.form.get("user_geolocation")
	message_type = request.form.get("message_type")
	user_contact_info = request.form.get("user_contact_info")


	vehicle_id = processes_line_and_bound_selects_closest_vehicle(line, bound)

	adds_to_queue(user_fname, user_lname, user_email, user_phone_num, destination_geo_location, message_type, vehicle_id)

	return render_template("/thank_you.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
