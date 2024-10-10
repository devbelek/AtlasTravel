from django.db import models
from django.utils.html import format_html
from django.core.files.base import ContentFile
from ckeditor.fields import RichTextField
from PIL import Image, ExifTags
import io
import os


def compress_image(image, max_size=(1920, 1080), quality=85, format='JPEG'):
    img = Image.open(image)

    # Сохраняем EXIF данные
    try:
        exif = img.info['exif']
    except KeyError:
        exif = None

    # Поворачиваем изображение согласно EXIF данным
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Изображение не имеет EXIF данных
        pass

    # Изменяем размер, сохраняя пропорции
    img.thumbnail(max_size, Image.LANCZOS)

    # Определяем формат
    if img.format == 'PNG' and img.mode == 'RGBA':
        format = 'PNG'
    else:
        format = 'JPEG'
        if img.mode != 'RGB':
            img = img.convert('RGB')

    # Сжимаем
    output = io.BytesIO()
    if format == 'JPEG':
        img.save(output, format=format, quality=quality, optimize=True, progressive=True)
    else:  # PNG
        img.save(output, format=format, optimize=True)

    # Добавляем EXIF данные обратно, если они были
    if exif:
        image = Image.open(output)
        image.info['exif'] = exif
        output = io.BytesIO()
        image.save(output, format=format, exif=exif)

    output.seek(0)
    return ContentFile(output.read())


class RestIdea(models.Model):
    tours = models.ManyToManyField('tours.Tour', related_name='rest_ideas', verbose_name='Туры')

    def __str__(self):
        return str(self.tours.all())

    class Meta:
        verbose_name = 'Идея для отдыха'
        verbose_name_plural = 'Идеи для отдыха'


class BestChoice(models.Model):
    tours = models.ManyToManyField('tours.Tour', related_name='best_choices', verbose_name='Туры')

    def __str__(self):
        return str(self.tours.all())

    class Meta:
        verbose_name = 'Лучшее предложение'
        verbose_name_plural = 'Лучшие предложения'


class PopularHotel(models.Model):
    hotels = models.ManyToManyField('hotels.Hotel', related_name='popular_hotels', verbose_name='Отели')

    def __str__(self):
        return str(self.hotels.all())

    class Meta:
        verbose_name = 'Популярный отель'
        verbose_name_plural = 'Популярные отели'


class RentOfCar(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', default='Аренда автомобиля')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Аренда автомобиля'
        verbose_name_plural = 'Аренда автомобилей'


class RentOfCarImage(models.Model):
    rent_of_car = models.ForeignKey(RentOfCar, related_name='images', on_delete=models.CASCADE,
                                    verbose_name='Аренда автомобиля')
    image = models.ImageField(upload_to='car_rentals/', verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    # Новые поля для настройки сжатия
    max_width = models.PositiveIntegerField(default=1920, verbose_name='Максимальная ширина')
    max_height = models.PositiveIntegerField(default=1080, verbose_name='Максимальная высота')
    quality = models.PositiveIntegerField(default=85, verbose_name='Качество (1-100)')

    class Meta:
        verbose_name = "Изображение аренды автомобиля"
        verbose_name_plural = "Изображения аренды автомобилей"
        ordering = ['order']

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="auto" />', self.image.url)
        return "-"

    image_tag.short_description = 'Превью'

    def save(self, *args, **kwargs):
        if self.image:
            # Получаем расширение файла
            ext = os.path.splitext(self.image.name)[1].lower()

            # Сжимаем изображение
            compressed_image = compress_image(
                self.image,
                max_size=(self.max_width, self.max_height),
                quality=self.quality,
                format='PNG' if ext == '.png' else 'JPEG'
            )

            # Сохраняем сжатое изображение
            self.image.save(self.image.name, compressed_image, save=False)

        super().save(*args, **kwargs)


class RentOfCarDescription(models.Model):
    rent_of_car = models.ForeignKey(RentOfCar, related_name='descriptions', on_delete=models.CASCADE,
                                    verbose_name='Аренда автомобиля')
    description = RichTextField(verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Описание аренды автомобиля"
        verbose_name_plural = "Описания аренды автомобилей"
        ordering = ['order']


class Benefits(models.Model):
    icon = models.FileField(verbose_name='Иконка')
    title = models.CharField(max_length=30, verbose_name='Заголовок')
    description = RichTextField(verbose_name='Описание')

    # Новые поля для настройки сжатия
    max_width = models.PositiveIntegerField(default=200, verbose_name='Максимальная ширина иконки')
    max_height = models.PositiveIntegerField(default=200, verbose_name='Максимальная высота иконки')
    quality = models.PositiveIntegerField(default=90, verbose_name='Качество (1-100)')

    class Meta:
        verbose_name = "Преимущество работы с нами"
        verbose_name_plural = "Преимущества работы с нами"

    def save(self, *args, **kwargs):
        if self.icon:
            # Получаем расширение файла
            ext = os.path.splitext(self.icon.name)[1].lower()

            # Проверяем, является ли файл изображением
            try:
                Image.open(self.icon)
            except IOError:
                # Если это не изображение, сохраняем как есть
                super().save(*args, **kwargs)
                return

            # Сжимаем изображение
            compressed_image = compress_image(
                self.icon,
                max_size=(self.max_width, self.max_height),
                quality=self.quality,
                format='PNG' if ext == '.png' else 'JPEG'
            )

            # Сохраняем сжатое изображение
            self.icon.save(self.icon.name, compressed_image, save=False)

        super().save(*args, **kwargs)