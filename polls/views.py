import json
import logging
import random
import requests

from celery.result import AsyncResult
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from polls.forms import YourForm
from polls.tasks import sample_task, task_process_notification

logger = logging.getLogger(__name__)



def subscribe(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            task = sample_task.delay(form.cleaned_data['email'])
            return JsonResponse({
                'task_id': task.task_id
            })
    form = YourForm()
    return render(request, 'form.html', {'form': form})


def task_status(request):
    task_id = request.GET.get('task_id')
    if task_id:
        task = AsyncResult(task_id)
        state = task.state

        if state == 'FAILURE':
            error = str(task.result)
            response = {
                'state': state,
                'error': error,
            }
        else:
            response = {
                'state': state,
            }
        return JsonResponse(response)    


@csrf_exempt
def webhook_test(request):
    if not random.choice([0, 1]):
        raise Exception('Why are you geh')
    requests.post('https://httbin.org/delay/5')
    return HttpResponse('pong')

@csrf_exempt
def webhook_test_async(request):
    task = task_process_notification.delay()
    logger.info(task.id)
    return HttpResponse('pong')