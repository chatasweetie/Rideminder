import twilio
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account

client = TwilioRestClient()
 
# need to add phone number from queue to be the "to="

message_with_3_blocks = client.messages.create(to="+15597314996", from_=TWILIO_NUMBER,
                                     body="You are within 3 blocks of your destination")

def send_text_message(phone):
	"""sends the text message to the user once the destination is within WALK_RADIUS"""
	
	try:
	    client = twilio.rest.TwilioRestClient(account_sid, auth_token)
	 
	    message = client.messages.create(
	        body="Hello World",
	        to="+14159352345",
	        from_="+14158141829"
	    )
	except twilio.TwilioRestException as e:
	    print e