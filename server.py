"""Transit Alert"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

import request

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "123"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Setting up my firebase connection 


@app.route("/")
def index():
    """Homepage."""
    

    return render_template("homepage.html")

@app.route("user_input", methods=["POST"])
def process_user_info():
	"""recieves the user data and sends data to appropiate processes"""
	username = request.form.get("username")
	line = request.form.get("line")
	destination_geo_location = request.form.get("destination_geo_location")
	user_geolocation = request.form.get("user_geolocation")
	message_type = request.form.get("message_type")
	user_contact_info = request.form.get("user_contact_info")

	
	functions to process N & Geolocation to bus_id
	
	
	
@app.route("input_user_db")
def 

