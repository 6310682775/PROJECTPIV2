# from celery.result import AsyncResult
from urllib import response
from django.contrib.auth import get_user_model
from celery import shared_task
from detect_and_track import mymain


# @shared_task
# def detection(data):
#     response = Detection_call(data)
#     return result, video(path)

# @shared_task
# def detection():
#     # response = Detection_call()
#     return "done"

@shared_task
def run_detect(loopfile, vdofile):
    saved_result = mymain(cmd=False, custom_arg=[
                          '--loop', loopfile, '--source', vdofile])
    return saved_result
