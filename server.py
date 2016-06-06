"""Transit Alert"""
import os
from jinja2 import StrictUndefined

from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

# from process_data import gets_a_list_of_available_line, processes_line_and_bound_selects_two_closest_vehicle, convert_to_e164, process_lat_lng_get_arrival_datetime, gets_agencies
from model import adds_to_queue, connect_to_db

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

    return render_template("homepage.html", agency_list=agency_list)


@app.route("/routes.json")
def routes():
    """returns agency's routes"""

    agency = request.arg.get("agency")

    routes = {
        route.marker_id: {
            "route_id": route.route_id,
            "name": route.name,
            "route_code": route.route_code,
            "direction": route.direction,
            "stop_list": route.stop_list,
            "agency_id": route.agency_id,
        }
        for route in Route.query.filter_by(agency_id=agency.agency_id).all()}

    return jsonify(routes)


@app.route("/thank-you", methods=["POST"])
def process_user_info():
    """recieves the user data and sends data to appropiate processes"""

    user_fname = request.form.get("fname")
    raw_user_phone_num = request.form.get("phone")
    agency = request.form.get("agency")
    route_code = request.form.get("route-code")
    direction = str(request.form.get("direction"))
    destination_stop_code = request.form.get("destination-stop-code")
    user_lat = request.form.get("lat")
    user_lon = request.form.get("lon")


    user_inital_stop_code = gets_user_stop(user_lat, user_lon, route, direction)

    user_trip = gets_user_itinerary(agency, route_code, direction, destination_stop_code, user_inital_stop_code)

    arrival_time_datetime = process_lat_lng_get_arrival_datetime(user_lat, user_lon, destination_stop_code)

    user_phone = convert_to_e164(raw_user_phone_num)

    adds_to_queue(user_fname, user_email, user_phone, user_lat, user_lon, destination_lat, destination_lon, vehicle_1, vehicle_1_distance, vehicle_2, vehicle_2_distance, arrival_time_datetime)

    if bound == "I":
        bound = "Inbound"
    else:
        bound = "Outbound"

    return render_template("/thank_you.html", user_fname=user_fname, user_phone=user_phone, bound=bound, line=line)



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
