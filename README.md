Awesome Name
--------


**Description**

Awesome_Name is a messaging system that will notify user when their transit vehicle is within three blocks of their destination via text message. 


### Screenshots

**Submit Request**
![alt text](https:// )

**Text Message**
![alt text](https:// )


### Technology Stack

**Application:** Python, Flask, Jinja, SQLAlchemy, Celery, RabbitMQ    
**APIs:** Firebase, Google Map, Twilio
**Front-End**: HTML/CSS, Bootstrap, JQuery, JavaScript, AJAX,    

### How to run https://cldup.com/-CCK9vvr9h.png locally

Create a virtual environment 

```
> virtualenv env
> source env/bin/activate
```

Install the dependencies

```
> pip install -r requirements.txt
```

Run the app 

```
> cd cd rabbitmq_server-3.5.6/
> sbin/rabbitmq-server 

New terminal 
> celery worker -l info --beat

New Terminal 
> python app.py


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