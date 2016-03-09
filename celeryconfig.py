# Configuration for Celery
import os
from celery.schedules import crontab

CELERY_TASK_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False
BROKER_PORT = 5672
BROKER_URL = os.environ.get('CLOUDAMQP_URL', 'amqp://')
CELERY_IMPORTS = ('tasks',)
CELERY_RESULT_BACKEND = None


CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.process_transit_request',
        'schedule': crontab(minute='*/1'),
    },
}
