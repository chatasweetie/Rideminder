Rideminder
--------


**Description**

Rideminder is a messaging system that will notify user when their transit vehicle is within three blocks of their destination via text message in San Fransisco. 


### Screenshot

**Submit Request**

<img src="static/Rideminder.jpg">


### Technology Stack

**Application:** Python, Flask, Jinja, SQLAlchemy, Celery, RabbitMQ    
**APIs:** Firebase, Google Map, Twilio  
**Front-End**: HTML/CSS, Bootstrap, JQuery, JavaScript, AJAX    

### UX Design
**Color:** Choosen to make accessable to persons with colorblindness     
**Font Size**: Large for persons with visual challenges     
**Font Type**: Dyslexia Typeface http://opendyslexic.org/g     


### How to run Rideminder locally

Download RabbitMQ server    
https://www.rabbitmq.com/


Create a virtual environment 

```
> virtualenv env
> source env/bin/activate
```

Install the dependencies

```
> pip install -r requirements.txt
```

Run RabbitMQ sever

```
> cd rabbitmq_server-3.5.6/
> sbin/rabbitmq-server 
```

In a new terminal run Celery worker
```
> celery worker -l info --beat
```

In a new Terminal run App
```
> python sever.py
```


Open your browser and navigate to 

```
http://localhost:5000/
```

Note: The messaging functionality requires that you have a Twilio account id, authorization token and phone number set as local environment variables:

```
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_NUMBER
```

Note: Rideminder can be modified to provide service for many large cities that Firebase support. For the complete list go to:

Firebase Data Sets: Transit https://publicdata-transit.firebaseio.com/

