import random
import requests

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

DUMMY_DELAY_API_URL = 'https://httpbin.com/delay/5'

def _api_call(email):
    if random.choice([0, 1]):
        raise Exception('Random processing error')
    requests.post(DUMMY_DELAY_API_URL)


@shared_task()
def sample_task(email):
    _api_call(email)


@shared_task(bind=True)
def task_process_notification(self):
    try:
        if random.choice([0, 1]):
            raise Exception()
        requests.post(DUMMY_DELAY_API_URL)
    except Exception as e:
        logger.error('Exception raised. It would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)