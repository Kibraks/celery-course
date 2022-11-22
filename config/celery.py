import os

from celery import Celery 
from celery.contrib import rdb
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery()

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def divide(x, y):
    import time
    rdb.set_trace()
    time.sleep(7)
    return x / y
