"""Class for my database to store user request"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class queue(db.Model):
	"""The queue holding request for notifications"""
	__tablename__ = "queue"
	
	queue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_name = db.Column(db.String(100), nullable=True)
	user_email = db.Column(db.String(100), nullable=True)
	user_phone_num = db.Column(db.Integer, nullable=True)
	vehicle_id = db.Column(db.Integer, nullable=False)
	destination_geo_location = db.Column(db.Integer, nullable=False)
	is_finished = db.Column(db.Boolean, default=False)

	def __repr__(self):
		"""Provides useful represenation when printed"""

		return "<Queue queue_id: {} user_name: {} vehicle id: {} is_finished: {}>".format(self.queue_id, 
								self.user_name, self.vehicle_id, self.is_finished)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///queue.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
	"""will connect to the db"""

    from server import app
    connect_to_db(app)
    print "Connected to DB."