# from celery.result import AsyncResult
from urllib import response
from django.contrib.auth import get_user_model
from celery import shared_task
import json


# @shared_task
# def detection(data):
#     response = Detection_call(data)
#     return result, video(path)

@shared_task
def detection():
    # response = Detection_call()
    return "done"
