from django import forms
from .models import Task, Loop
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateTimeInput, TimeInput
from django.core.exceptions import ValidationError


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['date_time', 'location', 'description',
                  'video_file', 'time']
        widgets = {
            'date_time': DateTimeInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
        }
    
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            if not video_file.name.endswith('.mp4'):
                raise ValidationError('Only MP4 files are allowed.')
        return video_file

class LoopForm(forms.ModelForm):
    class Meta:
        model = Loop
        fields = ['loop_name', 'loop_id', 'orientation',
                  'x_1', 'y_1', 'x_2', 'y_2', 'x_3', 'y_3', 'x_4', 'y_4',
                  'summary_location_x', 'summary_location_y']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
