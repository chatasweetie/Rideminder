Rideminder
--------
[Rideminder](http://rideminder.herokuapp.com)

**Description**

Rideminder is a messaging system that notifies user when they are either within 1/4 a mile or within 3 mins of their destination via text message. 

**How it works**

Designed to be used at transit stop and requires user’s transit line, transit stop and phone number. It makes 2 API calls for transit information:   

   *Firebase - gets realtime data of transit vehicles   
   *Google Map Direction - gets direction information    

<img src="static/img/firebase-deprecated.png" height="250">

[Updates on new Dataset](https://chatasweetie.wordpress.com/category/rideminder/)    

Rideminder analyses and processes two types of data - gets the closest transit vehicle number in realtime and creates a datetime object using the estimated arrival time. It places the information into my Postgres database.

The Celery worker (celery is an asynchronous task queue/job queue based on distributed message passing) pulls request that have not been completed from my database every minute. It checks the transit vehicle's current location if it is within ½ a mile of the user’s destination. It also checks the datetime object if the estimated time is within 3 mins. If either of these conditions are satisfied, it sends a text message to the user using Twilio.  



### Screenshot

**Submit Request**

<img src="static/img/rideminder_new_color.jpg">

**Submit Request Cell**

<img src="static/img/rideminder-cell.jpg" height="300">

**Thank You for Submission**

<img src="static/img/thank-you.jpg" >

**Thank You for Submission Cell**

<img src="static/img/thankyou-cell.jpg" height="300">


### Technology Stack

**Application:** Python, Flask, Jinja, SQLAlchemy, Celery, RabbitMQ, PostgreSQL    
**APIs:** Firebase, Google Map, Twilio, Google Map Direction  
**Front-End**: HTML/CSS, Bootstrap, JQuery, JavaScript, AJAX    


### Testing Coverage

<img src="static/img/coveragereportrideminder.png" height="250">


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

Run RabbitMQ server

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
> python server.py
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

Firebase Data Sets: [Transit](https://publicdata-transit.firebaseio.com/)


### About the Developer    
Jessica Dene Earley    
[Short Bio](https://chatasweetie.wordpress.com/about-me/)   
[Linkedin](https://www.linkedin.com/in/jessicaearley)    
[Blog of Rideminder](https://chatasweetie.wordpress.com/category/rideminder/)     
[Chatasweetie's Blog](https://chatasweetie.wordpress.com/)    
