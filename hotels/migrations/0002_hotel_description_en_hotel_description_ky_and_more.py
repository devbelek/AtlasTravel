# Generated by Django 5.0.6 on 2024-10-09 18:34

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='description_en',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='description_ky',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='description_ru',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Название отеля'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='title_ky',
            field=models.CharField(max_length=255, null=True, verbose_name='Название отеля'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Название отеля'),
        ),
    ]
