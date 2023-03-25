# from django.shortcuts import render
from django.http import JsonResponse
from mysite.tasks import *
import json
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Task, Loop, LoopResult, VehicleCount
from .forms import TaskForm, LoopForm
from django.core.files.base import ContentFile
import os
from django_celery_results.models import TaskResult
from celery.result import AsyncResult

from django.http import FileResponse
from django.shortcuts import get_object_or_404


def download_file(request, result_id):

    obj = get_object_or_404(LoopResult, pk=result_id)

    file = obj.summary_file.open('rb')

    response = FileResponse(file)

    response.content_type = 'text/csv'
    task_id = obj.task_loop_result.task_id
    loop_id = obj.loop_id
    response['Content-Disposition'] = f'attachment; filename="{task_id}_{loop_id}.csv"'

    return response


def download_video(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    video_path = task.video_result_file.path
    filename = task.video_file.name.split('/')[-1]
    response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def dashboard(request):
    tasks = Task.objects.all()
    task_status_data = []
    for task in tasks:
        if task.task_id_celery is not None:
            task_result = AsyncResult(task.task_id_celery)
            status = task_result.status
            task = Task.objects.get(pk=task.pk)
            task.state = status
        else:
            status = "UNPROCESS"
        task_status_data.append({
            'task_id': task.task_id,
            'location': task.location,
            'description': task.description,
            'date_time': task.date_time,
            'status': status,
            'task_id_celery': task.task_id_celery,
            'video_file': task.video_file,
        })

    return render(request, 'task/Dashboard.html', {'tasks': task_status_data})


def check_result(request):
    task_id = request.GET.get('task_id')
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return HttpResponse("success")
    else:
        return HttpResponse("processing")


def new_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:dashboard"))
    else:
        form = TaskForm()
    return render(request, 'task/NewTask.html', {'form': form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:dashboard"))
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/EditTask.html', {'form': form})


def new_loop(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = LoopForm(request.POST)
        if form.is_valid():
            loop = form.save(commit=False)
            loop.head_task = task
            loop.save()
            return redirect(reverse("main:loop_dashboard", args=(task_id,)))
    else:
        form = LoopForm(initial={'head_task': task})
    return render(request, 'loop/NewLoop.html', {'form': form, 'task_id': task_id})


def edit_loop(request, loop_id):
    loop = get_object_or_404(Loop, pk=loop_id)
    if request.method == 'POST':
        form = LoopForm(request.POST, instance=loop)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:loop_dashboard", args=(loop.head_task.pk,)))
    else:
        form = LoopForm(instance=loop)
    return render(request, 'loop/EditLoop.html', {'form': form, 'task_id': loop.head_task.pk})


def loop_dashboard(request, task_id):
    loops = Loop.objects.filter(head_task__pk=task_id)
    return render(request, 'loop/LoopDashboard.html', {'loops': loops, 'task_id': task_id})


def loops_to_json(task_id):
    loops = Loop.objects.filter(head_task__pk=task_id)
    loop_list = []
    for loop in loops:
        point_list = [
            {'x': loop.x_1, 'y': loop.y_1},
            {'x': loop.x_2, 'y': loop.y_2},
            {'x': loop.x_3, 'y': loop.y_3},
            {'x': loop.x_4, 'y': loop.y_4},
        ]
        summary_location = {'x': loop.summary_location_x,
                            'y': loop.summary_location_y}

        loop_dict = {
            'name': loop.loop_name,
            'id': loop.loop_id,
            'points': point_list,
            'orientation': loop.orientation,
            'summary_location': summary_location
        }

        loop_list.append(loop_dict)

    response_data = {'loops': loop_list}
    return response_data


def test_save_result(request, task_id):
    task = Task.objects.get(pk=task_id)
    counting_result_path = 'static/object_tracking15/loop.txt'
    video_result_path = 'static/object_tracking15/video2.mp4'
    counting_result_file = open(counting_result_path, 'rb')
    video_file = open(video_result_path, 'rb')
    task.video_result_file.save(os.path.basename(
        video_result_path), video_file, save=True)
    task.counting_result_file.save(os.path.basename(
        counting_result_path), counting_result_file, save=True)
    task.save()
    return redirect(reverse("main:dashboard"))


def call_detect(request, task_id):
    loopfile_demo = {
        "loops": [
            {
                "name": "loop1",
                "id": "0",
                "points": [
                    {"x": 900, "y": 600},
                    {"x": 900, "y": 300},
                    {"x": 400, "y": 300},
                    {"x": 400, "y": 600}
                ],
                "orientation": "counterclockwise",
                "summary_location": {"x": 20, "y": "20"}
            },
            {
                "name": "loop2",
                "id": "1",
                "points": [
                    {"x": 280, "y": 450},
                    {"x": 280, "y": 200},
                    {"x": 600, "y": 200},
                    {"x": 600, "y": 450}

                ],
                "orientation": "clockwise",
                "summary_location": {"x": 20, "y": "380"}
            },
            {
                "name": "loop3",
                "id": "2",
                "points": [
                    {"x": 600, "y": 80},
                    {"x": 850, "y": 80},
                    {"x": 900, "y": 600},
                    {"x": 600, "y": 600}

                ],
                "orientation": "clockwise",
                "summary_location": {"x": 950, "y": "20"}
            }
        ]
    }
    task = Task.objects.get(pk=task_id)
    loopfile = loops_to_json(task_id)
    vdofile = task.video_file.url.lstrip('/')
    task_result = run_detect.delay(vdofile, loopfile, task_id)
    task.task_id_celery = task_result.task_id
    # task.task_result = TaskResult.objects.get(task_id=task_result)
    task.save()

    return HttpResponse(task_result, content_type='application/json')


def get_result(request, task_id):
    loop_count = 3
    task = Task.objects.get(pk=task_id)
    # vehicle_counts = []
    # loop_results = []
    results = []
    for i in range(loop_count):
        vehicle_count = VehicleCount.objects.filter(
            loop_result__loop_id=i, loop_result__task_loop_result__task_id=task.task_id)
        loop_result = LoopResult.objects.get(
            loop_id=i, task_loop_result__task_id=task.task_id)
        # vehicle_counts.append(vehicle_count)
        # loop_results.append(loop_result)
        results.append((vehicle_count, loop_result))
    return render(request, 'task/CountingResult.html', {'results': results, 'task': task})
