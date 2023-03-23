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


class TaskResult(models.Model):
    task_id_celery = models.CharField(max_length=255, unique=True)
    date_done = models.DateTimeField(default=timezone.now)
    result = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    traceback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.task_id}: {self.status}'


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_id_celery = models.CharField(max_length=50)
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
    task_result = models.OneToOneField(
        TaskResult, on_delete=models.CASCADE, null=True)


# class Loop(models.Model):
#     loop_name = models.ForeignKey(Task, on_delete=models.CASCADE)
#     loop_id = models.IntegerField()
#     point_x_1 = models.IntegerField()
#     point_y_1 = models.IntegerField()
#     point_x_2 = models.IntegerField()
#     point_y_2 = models.IntegerField()
#     point_x_3 = models.IntegerField()
#     point_y_3 = models.IntegerField()
#     point_x_4 = models.IntegerField()
#     point_y_4 = models.IntegerField()
#     orientation = models.CharField(max_length=50)
#     summary_location_x = models.IntegerField()
#     summary_location_y = models.IntegerField()

class Loop(models.Model):
    head_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    loop_name = models.CharField(max_length=50)
    coordinates_x = models.IntegerField()
    coordinates_y = models.IntegerField()
