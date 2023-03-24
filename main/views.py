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
from .models import Task, Loop
from .forms import TaskForm, LoopForm
from django.core.files.base import ContentFile
import os


def dashboard(request):
    tasks = Task.objects.all()
    return render(request, 'task/Dashboard.html', {'tasks': tasks})


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

    task = Task.objects.get(pk=task_id)
    loopfile = loops_to_json(task_id)
    vdofile = task.video_file.url.lstrip('/')
    task_result = run_detect.delay(vdofile, loopfile, task_id)
    task.task_id_celery = task_result.task_id
    task.save()

    return HttpResponse(task_result, content_type='application/json')


def get_result(request, task_id):
    return
