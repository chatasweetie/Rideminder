import twilio
from twilio.rest import TwilioRestClient
import os 

# Find these values at https://twilio.com/user/account
TWILIO_ACCOUNT_SID=os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN=os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER=os.environ['TWILIO_NUMBER']


def send_text_message(phone):
	"""sends the text message to the user once the destination is within WALK_RADIUS"""
	
	try:
	    client = twilio.rest.TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
	 
	    message = client.messages.create(
	        body="You are within 3 blocks of your destination, thank you for using Rideminder",
	        to=phone,
	        from_=TWILIO_NUMBER
	    )
	except twilio.TwilioRestException as e:
	    print e