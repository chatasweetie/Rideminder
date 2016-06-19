"""Transit Alert"""
import os
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

# from process_data import gets_a_list_of_available_line, processes_line_and_bound_selects_two_closest_vehicle, convert_to_e164, process_lat_lng_get_arrival_datetime, gets_agencies
from model import connect_to_db, checks_user_db, adds_transit_request, gets_agency_db, Agency

from celery import Celery


app = Flask(__name__)

# Required t,l.o use Flask sessions and the debug toolbar
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")


# Make Jinja2 to raise an error instead of failing sliently
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage"""
    agencies = Agency.query.filter().all()

    agency_db = gets_agency_db('Caltrain')

    routes = agency_db.routes

    return render_template("homepage.html", agencies=agencies, routes=routes)


@app.route("/agency.json", methods=["GET"])
def routes():
    """returns agency's routes"""

    agency = request.args.get("agency")
    print agency

    agency_db = gets_agency_db(agency)
    print agency_db

    routes = {
        route.name: {
            "route_id": route.route_id,
            "name": route.name,
            "direction": route.direction,
        }
        for route in agency_db.routes}

    return jsonify(sorted(routes.items()))


@app.route("/thank-you", methods=["POST"])
def process_user_info():
    """recieves the user data and sends data to appropiate processes"""

    user_name = request.form.get("fname")
    raw_user_phone_num = request.form.get("phone")
    agency = request.form.get("agency")
    route_code = request.form.get("route-code")
    direction = request.form.get("direction")
    destination_stop = request.form.get("destination-stop")
    user_lat = request.form.get("lat")
    user_lon = request.form.get("lon")

    user_inital_stop = gets_user_stop_id(user_lat, user_lon, route_code, direction)

    user_itinerary = gets_user_itinerary(agency, route_code, direction, destination_stop, user_inital_stop)

    arrival_time_datetime = process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_stop)

    user_phone = convert_to_e164(raw_user_phone_num)

    user_db = checks_user_db(user_name, user_phone)

    adds_transit_request(user_inital_stop, destination_stop, agency, route_code, user_itinerary, arrival_time_datetime, user_db)


    return render_template("/thank_you.html", user_fname=user_fname, user_phone=user_phone, direction=direction, route_code=route_code)



# Celery is an open source asynchronous task queue/job queue based on distributed message passing.
# It is focused on real-time operation, but supports scheduling as well.
celery = Celery(app)

celery.config_from_object('celeryconfig')


if __name__ == "__main__":

    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
