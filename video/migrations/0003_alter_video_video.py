# Generated by Django 5.0.3 on 2024-03-23 10:48

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_video_video_alter_video_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='video'),
        ),
    ]