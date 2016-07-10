"""Class for my database to store user, transit request & transit info"""
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """This is an individual user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(100), nullable=True)
    user_phone = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<User user_name: {} >""".format(self.user_name)


class Transit_Request(db.Model):
    """This is the individual request for notification"""

    __tablename__ = "transit_requests"

    request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    inital_stop_code = db.Column(db.String(100), nullable=False)
    destination_stop_code = db.Column(db.String(100), nullable=False)
    agency = db.Column(db.String(100), nullable=False)
    route = db.Column(db.String(200), nullable=False)
    route_code = db.Column(db.String(200), nullable=False)
    user_itinerary = db.Column(db.String(5000), nullable=True)
    arrival_time = db.Column(db.DateTime, nullable=False)
    start_time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    end_time_stamp = db.Column(db.DateTime, nullable=True)
    is_finished = db.Column(db.Boolean, default=False)
    current_stop = db.Column(db.String(200), nullable=False)
    time_difference = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer,
                            db.ForeignKey("users.user_id"),
                            nullable=False)

    user = db.relationship("User",
                                backref=db.backref("transit_requests"))

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Transit Request request_id: {} user_inital_stop: {}
                    user_destination_stop: {} route: {}>""".format(self.request_id,
                    self.inital_stop_code, self.destination_stop_code, self.route)



class Agency(db.Model):
    """This is an individual Transit Agency"""

    __tablename__ = "agencies"

    agency_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    has_direction = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Agency name: {} has_direction: {}>".format(self.name,
                                                        self.has_direction)


class Route(db.Model):
    """This is an route/line for a Transit Agency"""

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    route_code = db.Column(db.String(100), nullable=False)
    direction = db.Column(db.String(100), nullable=False)
    stop_list = db.Column(db.String(5000), nullable=False)
    agency_id = db.Column(db.Integer,
                            db.ForeignKey("agencies.agency_id"),
                            nullable=False)

    agency = db.relationship("Agency",
                                backref=db.backref("routes",
                                order_by=route_id))

    stops = db.relationship("Stop",
                             secondary="routes_stops",
                             backref="routes")

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Route name: {} agency_id: {}>".format(self.name, self.agency_id)


class Stop(db.Model):
    """This is an individual stop for a variety of routes"""

    __tablename__ = "stops"

    stop_code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Stop name: {} >".format(self.name)


class Route_Stop(db.Model):
    """This is an individual route to an individual stop"""

    __tablename__ = "routes_stops"

    route_stop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer,
                            db.ForeignKey("routes.route_id"),
                            nullable=False)
    stop_id = db.Column(db.Integer,
                            db.ForeignKey("stops.stop_code"),
                            nullable=False)

    route = db.relationship("Route",
                                backref=db.backref("route_stops",
                                order_by=route_id))

    stops = db.relationship("Stop",
                             backref="route_stops")

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Route_Stop route id: {} stop id: {} stop name: {}>".format(
                                                                self.route_id,
                                                                self.stop_id,
                                                                self.stops)

##########################################################################
# Helper Functions


def checks_user_db(user_name, user_phone):
    """checks the db if the user is in the db and returns user object"""
    user = User.query.filter_by(user_phone=user_phone).first()

    if user:
        return user

    new_user = User(user_name=user_name, user_phone=user_phone)
    db.session.add(new_user)
    db.session.commit()

    return User.query.filter_by(user_phone=user_phone).first()


def adds_transit_request(user_inital_stop, destination_stop, agency, route,
    route_code, arrival_time_datetime, user_db):
    """adds a transit request to the database"""

    now = datetime.utcnow()
    new_transit_request = Transit_Request(inital_stop_code=user_inital_stop,
                destination_stop_code=destination_stop, agency=agency, route=route,
                route_code=route_code, arrival_time=arrival_time_datetime,
                start_time_stamp=now, current_stop=user_inital_stop,
                user_id=user_db.user_id)

    db.session.add(new_transit_request)
    db.session.commit()


def list_of_is_finished_to_process():
    """Gets all the transit_request that need to be processed (ie. is_finished = False)"""

    request_to_process = Transit_Request.query.filter(Transit_Request.is_finished == False).all()

    return request_to_process


def gets_agency_db(name):
    """returns the db object of an agency"""

    return Agency.query.filter_by(name=name).first()


def gets_route_db(route_code, direction=False):
    """returns the db object of a route"""

    if direction is False:
        return Route.query.filter_by(route_code=route_code).first()

    return Route.query.filter_by(route_code=route_code, direction=direction).first()


def gets_route_id_db(route_id):
    """returns the db object of a route"""

    return Route.query.filter_by(route_id=route_id).first()


def gets_stop_db(stop_id):
    """returns the db object of a stop"""

    return Stop.query.filter_by(stop_code=stop_id).first()


def gets_stop_name_db(stop_name):
    """returns the db object of a stop"""

    return Stop.query.filter_by(name=stop_name).all()


def records_request_vehicle_id_db(request, vehicle_id):
    """Sets the transit_request vehicle_id"""

    request.vehicle_id = int(vehicle_id)
    update_request(request)


def update_request(request):
    """Updates the request's information into the db"""

    db.session.commit()


def records_request_complete_db(request):
    """Changes the transit_request is_finished to True (request is complete)"""

    request.is_finished = True
    update_request(request)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql:///ridemindertest")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    """will connect to the db"""
    import os
    os.system("dropdb rideminder")
    os.system("createdb rideminder")
    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
