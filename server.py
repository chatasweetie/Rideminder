"""Transit Alert"""
import os
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, flash
from flask import redirect
from flask_debugtoolbar import DebugToolbarExtension
from flask import send_from_directory

from process_data import gets_user_stop_id, gets_user_itinerary, process_lat_lng_get_arrival_datetime, convert_to_e164
from model import connect_to_db, checks_user_db, adds_transit_request, gets_agency_db, Agency, gets_route_db, gets_route_id_db, gets_stop_db

from celery import Celery


app = Flask(__name__)

# Required t,l.o use Flask sessions and the debug toolbar
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")


# Make Jinja2 to raise an error instead of failing sliently
app.jinja_env.undefined = StrictUndefined


@app.route('/logo.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'logo.png', mimetype='image/png')


@app.route("/")
def index():
    """Homepage"""
    agencies = Agency.query.filter().all()

    return render_template("homepage.html", agencies=agencies)


@app.route("/agency.json", methods=["GET"])
def routes():
    """returns agency's routes"""

    agency = request.args.get("agency")

    agency_db = gets_agency_db(agency)

    routes = {
        route.name: {
            "route_id": route.route_id,
            "name": route.name,
            "direction": route.direction,
        }
        for route in agency_db.routes}

    return jsonify(sorted(routes.items()))


@app.route("/route.json", methods=["GET"])
def stops():
    """returns routes's stops"""

    route_id = request.args.get("route_id")

    route_db = gets_route_id_db(route_id)

    stops = {
        stop.name: {
            "stop_code": stop.stop_code,
            "name": stop.name,
            "lat": stop.lat,
            "lon": stop.lon,
        }
        for stop in route_db.stops}

    return jsonify(stops)


@app.route("/thank-you", methods=["POST"])
def process_user_info():
    """recieves the user data and sends data to appropiate processes"""

    user_name = request.form.get("name")
    raw_user_phone_num = request.form.get("phone")
    agency = request.form.get("agency")
    route_code = request.form.get("route")
    user_inital_stop = request.form.get("user_stop")
    destination_stop = request.form.get("destination_stop")
    user_lat = request.form.get("lat")
    user_lon = request.form.get("lng")

    if user_lat:
        user_inital_stop = gets_user_stop_id(user_lat, user_lon, route_code)

    else:
        user_inital_stop = gets_stop_db(user_inital_stop)
        user_lat = user_inital_stop.lat
        user_lon = user_inital_stop.lon

    print 'user_inital_stop:', user_inital_stop
    print 'A', agency
    print 'route_code', route_code
    print 'destin', destination_stop
    user_itinerary = '12, 24, 42'
    # user_itinerary = gets_user_itinerary(agency, route_code, destination_stop,
    #                                                             user_inital_stop)
    print "ITINERARY", user_itinerary
    if not user_itinerary:
        flash("You are too far away from your transit stop, try again when your closer")
        return redirect("/")

    arrival_time_datetime = process_lat_lng_get_arrival_datetime(user_lat, user_lon,
                                                                destination_stop)
    print "ARRIVAL TIME:", arrival_time_datetime
    user_phone = convert_to_e164(raw_user_phone_num)

    user_db = checks_user_db(user_name, user_phone)
    print "USER", user_db
    route = gets_route_id_db(route_code)

    adds_transit_request(user_inital_stop, destination_stop, agency, route.name,
                        route.route_code, user_itinerary, arrival_time_datetime, user_db)
    print "added to db"
    user_inital_stop = gets_stop_db(user_inital_stop)
    destination_stop = gets_stop_db(destination_stop)

    return render_template("/thank_you.html", user_fname=user_name, user_phone=user_phone,
            route=route, user_inital_stop=user_inital_stop, destination_stop=destination_stop)



############################################################################
# Error Pages
@app.errorhandler(404)
def page_not_found(error):
    """404 Page Not Found handling"""

    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    """500 Error handling """

    return render_template('/errors/500.html'), 500


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
