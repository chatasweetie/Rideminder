"""Class for my database to store user request"""
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transit_Request(db.Model):
	"""This is the individual request for notification"""

	__tablename__ = "transit_request"

	request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_fname = db.Column(db.String(100), nullable=True)
	user_lname = db.Column(db.String(100), nullable=True)
	user_email = db.Column(db.String(100), nullable=True)
	user_phone = db.Column(db.String(100), nullable=False)
	vehicle_id = db.Column(db.Integer, nullable=False)
	destination_lat = db.Column(db.Integer, nullable=False)
	destination_lon = db.Column(db.Integer, nullable=False)
	# start_time = db.Column(db.Time, nullable=False)
	# end_time = db.Column(db.Time, nullable=False)
	is_finished = db.Column(db.Boolean, default=False)
    
	def __repr__(self):
		"""Provides useful represenation when printed"""

		return "<Transit Request request_id: {} user_fname: {} vehicle id: {} is_finished: {}>".format(self.request_id, self.user_fname, self.vehicle_id, self.is_finished)

##########################################################################
# Helper Functions 

def adds_to_queue(user_fname, user_lname, user_email, user_phone, vehicle_id, destination_lat, destination_lon):
	"""Takes the form data and inputs into the transit_request database"""
	transit_request = Transit_Request(user_fname=user_fname, user_lname=user_lname, user_email=user_email, user_phone=user_phone, vehicle_id=vehicle_id, destination_lat=destination_lat, destination_lon=destination_lon)
	db.session.add(transit_request)
	db.session.commit()


def list_of_is_finished_to_process():
	"""Gets all the transit_request that need to be processed (ie. is_finished = False)"""
	request_to_process = Transit_Request.query.filter(Transit_Request.is_finished == False).all()

	return request_to_process


def records_request_complete_db(request):
	"""Changes the transit_request is_finished to True (request is complete)"""
	request.is_finished = True
	db.session.commit()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql:///rideminder")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transit.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
	"""will connect to the db"""

	from server import app
	connect_to_db(app)
	db.create_all()
	print "Connected to DB."