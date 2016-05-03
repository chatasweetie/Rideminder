"""Class for my database to store user request"""
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Transit_Request(db.Model):
    """This is the individual request for notification"""

    __tablename__ = "transit_request"

    request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_fname = db.Column(db.String(100), nullable=True)
    user_email = db.Column(db.String(100), nullable=True)
    user_phone = db.Column(db.String(100), nullable=False)
    user_lat = db.Column(db.Integer, nullable=False)
    user_lon = db.Column(db.Integer, nullable=False)
    destination_lat = db.Column(db.Integer, nullable=False)
    destination_lon = db.Column(db.Integer, nullable=False)

    vehicle_1 = db.Column(db.Integer, nullable=True)
    vehicle_1_distance = db.Column(db.Integer, nullable=True)
    vehicle_2 = db.Column(db.Integer, nullable=True)
    vehicle_2_distance = db.Column(db.Integer, nullable=True)

    vehicle_id = db.Column(db.Integer, nullable=False)

    arrival_time = db.Column(db.Integer, nullable=False)

    finished_timestamp_difference = db.Column(db.Integer, nullable=True)
    finished_vehicle_difference = db.Column(db.Integer, nullable=True)
    is_finished = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provides useful represenation when printed"""

        return """<Transit Request request_id: {} user_fname: {} vehicle id:
                    {} is_finished: {}>""".format(self.request_id, self.user_fname,
                    self.vehicle_id, self.is_finished)


class Agency(db.model):
    """This is an individual Transit Agency"""

    __tablename__ = "agencies"

    agency_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    has_direction = db.Column(db.Boolean, default=True)

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Agency name: {} has_direction: {}>".format(self.name,
                                                        self.has_direction)


class Route(db.model):
    """This is an route/line for a Transit Agency"""

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    agency_name = db.relationship("Agency",
                                backref=db.backref("routes", order_by=route_id))

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Route name: {} agency_id: {}>".format(self.name, self.agency_id)


class Stop(db.model):
    """This is an individual stop for a variety of routes"""

    __tablename__ = "stops"

    stop = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    lat = db.Column(db.Integer, nullable=False)
    lon = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Stop name: {} >".format(self.name)


class Route_Stop(db.model):
    """This is an individual route to an individual stop"""

    __tablename__ = "routes_stops"

    route_stop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    route_id = db.relationship("Route",
                                backref=db.backref("routes", order_by=route_id))

    stop_id = db.relationship("Stop",
                                backref=db.backref("route_stop", order_by=stop))

    def __repr__(self):
        """Provides useful represenation when printed"""

        return "<Route_Stop id: {} route id: {} stop id: {}>".format(self.name,
                                                    self.route_id, self.stop_id)

##########################################################################
# Helper Functions

def adds_to_queue(user_fname, user_email, user_phone, user_lat, user_lon, destination_lat, destination_lon, vehicle_1, vehicle_1_distance, vehicle_2, vehicle_2_distance, arrival_time_datetime):
    """Takes the form data and inputs into the transit_request database"""

    new_transit_request = Transit_Request(user_fname=user_fname, user_email=user_email, user_phone=user_phone, user_lat=user_lat, user_lon=user_lon, destination_lat=destination_lat, destination_lon=destination_lon, vehicle_1=vehicle_1, vehicle_1_distance=vehicle_1_distance, vehicle_2=vehicle_2, vehicle_2_distance=vehicle_2_distance, arrival_time=arrival_time_datetime)
    db.session.add(new_transit_request)
    db.session.commit()
    print "added to db"


def list_of_is_finished_to_process():
    """Gets all the transit_request that need to be processed (ie. is_finished = False)"""

    request_to_process = Transit_Request.query.filter(Transit_Request.is_finished == False).all()

    return request_to_process


def records_request_vehicle_id_db(request, vehicle_id):
    """Sets the transit_request vehicle_id"""

    request.vehicle_id = int(vehicle_id)
    db.session.commit()


def records_time_and_distance(request, vehicle_difference, timestamp_difference):
    """Changes the transit_request is_finished to True (request is complete)"""

    request.finished_timestamp_difference = timestamp_difference
    request.finished_vehicle_difference = vehicle_difference
    db.session.commit()


def records_request_complete_db(request):
    """Changes the transit_request is_finished to True (request is complete)"""

    request.is_finished = True
    db.session.commit()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql://localhost/rideminder")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    """will connect to the db"""

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
