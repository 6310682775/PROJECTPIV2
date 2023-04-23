# from django.shortcuts import render
import matplotlib.pyplot as plt
import matplotlib
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
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import os
import zipfile
from django.http import HttpResponse
import io
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import imageio.v3 as iio
from django.conf import settings
from PIL import Image, ImageDraw
import base64
from io import BytesIO
import cv2
import numpy as np
media_url = settings.MEDIA_URL
matplotlib.use('Agg')


def preview_loop_image(task, loops, task_id):
    image_path = task.image_file
    image = Image.open(image_path)

    # Draw a box on the image if there are loops
    if loops:
        loopfile = loops_to_json(task_id)
        img_array = np.array(image)
        image_draw = draw_loops_test(img_array, loopfile)
        image = Image.fromarray(image_draw)

    # Set figure size
    fig = plt.figure(figsize=(10, 10))

    # Plot the image with aspect ratio set to 'equal'
    plt.imshow(np.array(image), aspect='equal')

    # Set x and y axis scales
    plt.xticks(ticks=range(0, image.size[0], 100))
    plt.yticks(ticks=range(0, image.size[1], 100))

    # Set x and y axis labels
    plt.xlabel('X Scale')
    plt.ylabel('Y Scale')

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Convert the buffer to a base64-encoded string
    encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')

    return encoded_image


def draw_loops_test(img, loopfile):
    count_boxes = loopfile
    loops = count_boxes["loops"]
    for loop in loops:
        pt0, pt1, pt2, pt3 = loop["points"]

        cv2.line(img, (pt0["x"], pt0["y"]), (pt1["x"],
                 pt1["y"]), (255, 0, 0), 2)  # entering line
        cv2.line(img, (pt1["x"], pt1["y"]), (pt2["x"],
                 pt2["y"]), (255, 255, 0), 2)  # left line
        cv2.line(img, (pt2["x"], pt2["y"]), (pt3["x"],
                 pt3["y"]), (255, 255, 0), 2)  # straight
        cv2.line(img, (pt3["x"], pt3["y"]), (pt0["x"],
                 pt0["y"]), (255, 255, 0), 2)  # right
        cv2.putText(img, loop["name"], (pt0["x"], pt0["y"]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0, 255, 0], 2)

    return (img)


def new_loop(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    loops = Loop.objects.filter(head_task__pk=task_id)

    if request.method == 'POST':
        form = LoopForm(request.POST)
        if form.is_valid():
            loop = form.save(commit=False)
            loop.head_task = task
            loop.save()
            return redirect(reverse("main:loop_dashboard", args=(task_id,)))
    else:
        form = LoopForm(initial={'head_task': task})

    encoded_image = preview_loop_image(task, loops, task_id)

    return render(request, 'loop/NewLoop.html', {'form': form, 'task_id': task_id, 'encoded_image': encoded_image})


def edit_loop(request, loop_id, task_id):
    loop = get_object_or_404(Loop, pk=loop_id)
    task = Task.objects.get(pk=task_id)

    encoded_image = preview_loop_image(task, loop, task_id)

    if request.method == 'POST':
        form = LoopForm(request.POST, instance=loop)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:loop_dashboard", args=(loop.head_task.pk,)))
    else:
        form = LoopForm(instance=loop)
    return render(request, 'loop/EditLoop.html', {'form': form, 'task_id': loop.head_task.pk, 'encoded_image': encoded_image})


def loop_dashboard(request, task_id):
    loops = Loop.objects.filter(head_task__pk=task_id)
    task = Task.objects.get(pk=task_id)

    encoded_image = preview_loop_image(task, loops, task_id)

    return render(request, 'loop/LoopDashboard.html', {'loops': loops, 'task_id': task_id, 'task': task, 'encoded_image': encoded_image})


def new_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            video_file = task.video_file.path
            img_path = os.path.join(
                settings.MEDIA_ROOT, 'result', 'images', f"{task.task_id}.png")

            for frame_count, frame in enumerate(iio.imiter(video_file)):
                iio.imwrite(img_path, frame, format='png')
                if frame_count == 0:
                    break

            # save the image file path in the database
            task.image_file = img_path
            task.save()

            return redirect(reverse("main:dashboard"))
    else:
        form = TaskForm()
    return render(request, 'task/NewTask.html', {'form': form})


def signup_view(request):
    if (request.user.is_authenticated):
        return redirect('main:home')
    else:
        form = CreateUserForm()
        if (request.method == 'POST'):
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(
                    request, 'Successful you can login as username: ' + user)
                return redirect('main:login')

        context = {'form': form}
        return render(request, 'authenticate/signup.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'authenticate/home.html')
        else:
            messages.info(request, "Username or Password is incorrect.")
    return render(request, 'authenticate/login.html')


def logout_view(request):
    logout(request)
    return redirect('main:login')


def home_page(request):
    return render(request, 'authenticate/home.html')


def account_page(request):
    username = request.user.username
    context = {'name': username}
    return render(request, 'authenticate/account.html', context)


def account_page(request):
    username = request.user.username
    context = {'name': username}
    return render(request, 'authenticate/account.html', context)


def download_file(request, result_id):
    obj = get_object_or_404(LoopResult, pk=result_id)
    file = obj.summary_file.open('rb')
    response = FileResponse(file)
    response.content_type = 'text/csv'
    task_id = obj.task_loop_result.task_id
    loop_id = obj.loop_id
    response['Content-Disposition'] = f'attachment; filename="{task_id}_{loop_id}.csv"'

    return response


def download_raw_file(request, task_id):
    obj = get_object_or_404(Task, task_id=task_id)
    file = obj.counting_result_file.open('rb')
    response = FileResponse(file)
    response.content_type = 'text/csv'
    response['Content-Disposition'] = f'attachment; filename="{obj.task_id}.txt"'
    return response


def download_video(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    video_path = task.video_result_file.path
    filename = task.video_file.name.split('/')[-1]
    response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def download_all_file(request, task_id):
    directory_path = f"media/result/summary/{task_id}/"

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zip_file:
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                zip_file.write(file_path, file_name)

    zip_file_name = f"{task_id}.zip"

    response = HttpResponse(buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={zip_file_name}"

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
            'time': task.time,
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


def delete_task(request, task_id):

    task = get_object_or_404(Task, task_id=task_id)

    task.delete()

    return redirect(reverse("main:dashboard"))


def delete_loop(request, loop_id):

    loop = get_object_or_404(Loop, pk=loop_id)

    loop.delete()

    return redirect(reverse("main:loop_dashboard", args=(loop.head_task.pk,)))


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
    task.save()

    return redirect(reverse("main:dashboard"))


def get_result(request, task_id):
    loop_count = 3
    task = Task.objects.get(pk=task_id)
    results = []
    for i in range(loop_count):
        vehicle_count = VehicleCount.objects.filter(
            loop_result__loop_id=i, loop_result__task_loop_result__task_id=task.task_id)
        loop_result = LoopResult.objects.get(
            loop_id=i, task_loop_result__task_id=task.task_id)
        results.append((vehicle_count, loop_result))
    return render(request, 'task/CountingResult.html', {'results': results, 'task': task})


def search(request):
    tasks = Task.objects.all()

    query = request.GET.get('location')
    if query:
        tasks = tasks.filter(location__icontains=query)

    date = request.GET.get('date')
    if date:
        tasks = tasks.filter(date_time__icontains=date)

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
            'time': task.time,
            'task_id_celery': task.task_id_celery,
            'video_file': task.video_file,
        })
    context = {
        'tasks': task_status_data,
        'query': query,
        'date': date,
    }

    return render(request, 'task/Dashboard.html', context)


def notifications(request):
    tasks = Task.objects.all()
    task_status_data = []
    success_tasks = []
    for task in tasks:
        if task.task_id_celery is not None:
            task_result = AsyncResult(task.task_id_celery)
            status = task_result.status
            task = Task.objects.get(pk=task.pk)
            task.state = status
        else:
            status = "UNPROCESS"
        task_status_data.append({
            'status': status,
            'task_id': task.task_id,
            'location': task.location,
        })

        if status == "SUCCESS":  # If the task status is "SUCCESS", add it to the list
            success_tasks.append(task)

    # if len(success_tasks) > 0: # If there are any tasks with a status of "SUCCESS"
    #     messages.success(request, "Work status is SUCCESS!") # send a success message

    return render(request, 'task/Notifications.html', {'tasks': task_status_data})
