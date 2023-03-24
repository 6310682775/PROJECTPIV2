from django.db import models
from django.utils import timezone
# Create your models here.


class Direction(models.Model):
    left = models.IntegerField()
    right = models.IntegerField()
    straight = models.IntegerField()


class Vehicle(models.Model):
    vehicle_total = models.IntegerField()
    vehicle_type = models.CharField(max_length=50)
    direction = models.OneToOneField(Direction, on_delete=models.CASCADE)


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_id_celery = models.CharField(max_length=50, null=True)
    date_time = models.CharField(max_length=50)
    date_time_modify = models.DateTimeField(auto_now=True)
    date_time_upload = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default="UNPROCESS")
    video_file = models.FileField(upload_to='videos/')
    time = models.CharField(max_length=50)
    vehicle = models.OneToOneField(
        Vehicle, on_delete=models.CASCADE, null=True)
    video_result_file = models.FileField(upload_to='result/video/', null=True)
    counting_result_file = models.FileField(
        upload_to='result/counting/', null=True)


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
