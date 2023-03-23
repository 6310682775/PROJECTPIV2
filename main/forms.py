from django import forms
from .models import Task, Loop


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['date_time', 'location', 'description',
                  'status', 'video_file', 'time']


class LoopForm(forms.ModelForm):

    class Meta:
        model = Loop
        fields = ('height', 'width', 'loop_name',
                  'coordinates_x', 'coordinates_y')


# class LoopForm(forms.ModelForm):
#     class Meta:
#         model = Loop
#         fields = ['loop_name', 'loop_id', 'point_x_1', 'point_y_1', 'point_x_2', 'point_y_2', 'point_x_3', 'point_y_3', 'point_x_4', 'point_y_4', 'orientation', 'summary_location_x', 'summary_location_y']
