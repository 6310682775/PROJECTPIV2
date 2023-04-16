from django.db import models
from django.utils import timezone
from django_celery_results.models import TaskResult
# Create your models here.
from django.core.validators import FileExtensionValidator


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_id_celery = models.CharField(max_length=50, null=True)
    date_time = models.CharField(max_length=50)
    date_time_modify = models.DateTimeField(auto_now=True)
    date_time_upload = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    time = models.CharField(max_length=50)
    video_result_file = models.FileField(upload_to='result/video/', null=True)
    counting_result_file = models.FileField(
        upload_to='result/counting/', null=True)
    state = models.CharField(max_length=50)
    image_file = models.ImageField(upload_to='images/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], null=True)


class LoopResult(models.Model):
    task_loop_result = models.ForeignKey(
        Task, on_delete=models.CASCADE)
    loop_id = models.IntegerField()
    summary_file = models.FileField(
        upload_to='result/summary/', null=True)


class VehicleCount(models.Model):
    loop_result = models.ForeignKey(
        LoopResult, on_delete=models.CASCADE)
    loop_id = models.IntegerField()
    vehicle_type = models.CharField(max_length=50)
    entered = models.IntegerField()
    straight = models.IntegerField()
    right = models.IntegerField()
    left = models.IntegerField()


class Loop(models.Model):
    head_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    loop_name = models.CharField(max_length=255)
    loop_id = models.IntegerField()
    orientation = models.CharField(max_length=255)
    x_1 = models.IntegerField()
    y_1 = models.IntegerField()
    x_2 = models.IntegerField()
    y_2 = models.IntegerField()
    x_3 = models.IntegerField()
    y_3 = models.IntegerField()
    x_4 = models.IntegerField()
    y_4 = models.IntegerField()
    summary_location_x = models.IntegerField()
    summary_location_y = models.IntegerField()
    def __str__(self):
        return self.loop_name
