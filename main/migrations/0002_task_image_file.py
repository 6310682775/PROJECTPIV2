# Generated by Django 4.1.1 on 2023-04-15 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='image_file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
