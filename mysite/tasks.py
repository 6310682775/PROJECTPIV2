# from celery.result import AsyncResult
from urllib import response
from django.contrib.auth import get_user_model
from celery import shared_task
from detect_and_track import mymain
from main.models import Task
import os

# @shared_task
# def detection(data):
#     response = Detection_call(data)
#     return result, video(path)

# @shared_task
# def detection():
#     # response = Detection_call()
#     return "done"


@shared_task
def run_detect(vdofile, loopfile, task_id):
    saved_result = mymain(loopfile, cmd=False, custom_arg=[
                          '--source', vdofile])
    task = Task.objects.get(pk=task_id)
    counting_result_path, video_result_path = saved_result
    counting_result_file = open(counting_result_path, 'rb')
    video_file = open(video_result_path, 'rb')
    task.video_result_file.save(f"{task_id}.mp4", video_file, save=True)
    task.counting_result_file.save(
        f"{task_id}.txt", counting_result_file, save=True)
    task.save()
    counting_result_file.close()
    video_file.close()
    # Do something with the results
    # else:
    #     # The task is still running
    #     pass
    return saved_result


def save_result_to_task(saved_result, task_id):
    task = Task.objects.get(pk=task_id)
    counting_result_path, video_result_path = saved_result
    counting_result_file = open(counting_result_path, 'rb')
    video_file = open(video_result_path, 'rb')
    task.video_result_file.save(f"{task_id}.mp4", video_file, save=True)
    task.counting_result_file.save(
        f"{task_id}.txt", counting_result_file, save=True)
    task.save()
    counting_result_file.close()
    video_file.close()
