# Generated by Django 4.1.1 on 2023-05-14 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loop',
            name='orientation',
            field=models.CharField(choices=[('COUNTERCLOCKWISE', 'counterclockwise'), ('CLOCKWISE', 'clockwise')], max_length=20),
        ),
    ]
