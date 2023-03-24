# Generated by Django 4.1.1 on 2023-03-24 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left', models.IntegerField()),
                ('right', models.IntegerField()),
                ('straight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_total', models.IntegerField()),
                ('vehicle_type', models.CharField(max_length=50)),
                ('direction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.direction')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_id_celery', models.CharField(max_length=50, null=True)),
                ('date_time', models.CharField(max_length=50)),
                ('date_time_modify', models.DateTimeField(auto_now=True)),
                ('date_time_upload', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('status', models.CharField(default='UNPROCESS', max_length=50)),
                ('video_file', models.FileField(upload_to='videos/')),
                ('time', models.CharField(max_length=50)),
                ('video_result_file', models.FileField(upload_to=None)),
                ('counting_result_file', models.FileField(upload_to=None)),
                ('vehicle', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Loop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loop_name', models.CharField(max_length=255)),
                ('loop_id', models.IntegerField()),
                ('orientation', models.CharField(max_length=255)),
                ('x_1', models.IntegerField()),
                ('y_1', models.IntegerField()),
                ('x_2', models.IntegerField()),
                ('y_2', models.IntegerField()),
                ('x_3', models.IntegerField()),
                ('y_3', models.IntegerField()),
                ('x_4', models.IntegerField()),
                ('y_4', models.IntegerField()),
                ('summary_location_x', models.IntegerField()),
                ('summary_location_y', models.IntegerField()),
                ('head_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.task')),
            ],
        ),
    ]
