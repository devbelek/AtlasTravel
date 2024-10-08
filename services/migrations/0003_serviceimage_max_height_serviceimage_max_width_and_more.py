# Generated by Django 5.0.6 on 2024-10-10 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_servicefeature_description_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceimage',
            name='max_height',
            field=models.PositiveIntegerField(default=1080, verbose_name='Максимальная высота'),
        ),
        migrations.AddField(
            model_name='serviceimage',
            name='max_width',
            field=models.PositiveIntegerField(default=1920, verbose_name='Максимальная ширина'),
        ),
        migrations.AddField(
            model_name='serviceimage',
            name='quality',
            field=models.PositiveIntegerField(default=85, verbose_name='Качество (1-100)'),
        ),
    ]
