# Generated by Django 5.0.6 on 2024-10-10 01:05

import about.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0004_remove_aboutus_youtube_video_url_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutusimage',
            name='image',
            field=models.ImageField(upload_to='about_images/', validators=[about.models.validate_file_size], verbose_name='Изображение'),
        ),
    ]
