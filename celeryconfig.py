# Configuration for Celery
import os

CELERY_IMPORTS = ('tasks')
CELERY_IGNORE_RESULT = False
BROKER_HOST = "127.0.0.1" #IP address of the server running RabbitMQ and Celery
BROKER_PORT = 5672
BROKER_URL=os.environ.get('CLOUDAMQP_URL', 'amqp://')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS=("tasks",)

from celery.schedules import crontab
 
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.process_transit_request',
        'schedule': crontab(minute='*/1'),
    },
}

app.BROKER_POOL_LIMIT = 1