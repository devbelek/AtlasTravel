from django.db import models
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


class VisaService(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=255, verbose_name='Подзаголовок')
    description = RichTextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Визовая услуга'
        verbose_name_plural = 'Визовые услуги'

    def __str__(self):
        return self.title


class ServiceImage(models.Model):
    service = models.ForeignKey(VisaService, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='visa_services/', verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')

    # Новые поля для настройки сжатия
    max_width = models.PositiveIntegerField(default=1920, verbose_name='Максимальная ширина')
    max_height = models.PositiveIntegerField(default=1080, verbose_name='Максимальная высота')
    quality = models.PositiveIntegerField(default=85, verbose_name='Качество (1-100)')

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение услуги'
        verbose_name_plural = 'Изображения услуг'

    def __str__(self):
        return f"Изображение: {self.service.title}, Главное: {'Да' if self.is_main else 'Нет'}"

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


class ServiceFeature(models.Model):
    service = models.ForeignKey(VisaService, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = RichTextField(verbose_name='Описание')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Особенность услуги'
        verbose_name_plural = 'Особенности услуг'

    def __str__(self):
        return self.title