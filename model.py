"""Class for my database to store user request"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transit_Request(db.Model):
	"""This is the individual request for notification, aka queue"""

	__tablename__ = "transit_request"
	
	request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_fname = db.Column(db.String(100), nullable=True)
	user_lname = db.Column(db.String(100), nullable=True)
	user_email = db.Column(db.String(100), nullable=True)
	user_phone_num = db.Column(db.Integer, nullable=False)
	vehicle_id = db.Column(db.Integer, nullable=False)
	destination_geo_location = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.String(100), db.ForeignKey('transit_request.user_id'), nullable = True)
	is_finished = db.Column(db.Boolean, default=False)

	#Defines the relationship from users to queue
    # user = db.relationship("User", backref=db.backref("transit_request", order_by=user_id))
	
	def complete():
		"""When a transit_request has been completed, it is updated in the database as True"""
		db.session.excute(self._UPDATE, {"is_finished":True})
		db.session.commit()
    

	def __repr__(self):
		"""Provides useful represenation when printed"""

		return "<Transit Request request_id: {} user_fname: {} vehicle id: {} is_finished: {}>".format(self.request_id, self.user_fname, self.vehicle_id, self.is_finished)

class User(db.Model):
	"""Users that use the Transit_Request"""

	__tablename__ = "user"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	first_name = db.Column(db.String(100), nullable = False)
	last_name = db.Column(db.String(100), nullable = False)
	email = db.Column(db.String(100), nullable = False)
	phone_num = db.Column(db.Integer)
	password = db.Column(db.String(100), nullable = False)


	def __repr__(self):
		"""Provides useful represenation when printed"""

		return "<User user_id: {} first_name: {} last_name: {} email: {}>".format(self.user_id, self.user_name, self.vehicle_id, self.is_finished)


def adds_to_queue(user_fname, user_lname, user_email, user_phone_num, destination_geo_location, vehicle_id):
	"""Takes the form data and inputs into the transit_request database"""
	
	transit_request = Transit_Request(user_fname=user_fname, user_lname=user_lname, user_email=user_email, user_phone_num=user_phone_num, destination_geo_location=destination_geo_location, vehicle_id=vehicle_id)

	db.session.add(transit_request)
	db.session.commit()


def list_of_queue_to_process():
	"""Gets all the transit_request that need to be processed (ie. is_finished = False)"""

	in_query = Transit_Request.query.filter(Transit_Request.is_finished == "false")

	return in_query


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transit.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
	"""will connect to the db"""

	from server import app
	connect_to_db(app)
	db.create_all()
	print "Connected to DB."