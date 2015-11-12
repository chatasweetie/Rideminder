import twilio
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account

def send_text_message(phone):
	"""sends the text message to the user once the destination is within WALK_RADIUS"""
	
	try:
	    client = twilio.rest.TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
	 
	    message = client.messages.create(
	        body="I have your vehicle!",
	        to=phone,
	        from_=TWILIO_NUMBER
	    )
	except twilio.TwilioRestException as e:
	    print e