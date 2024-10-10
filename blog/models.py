from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.files.storage import default_storage
from django.conf import settings
import os


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB
        raise ValidationError("Максимальный размер файла 10MB")


def compress_image(image, max_size=(1200, 1200), quality=85):
    if image.size > (1 * 1024 * 1024):  # Если файл больше 1MB
        im = Image.open(image)
        output = BytesIO()

        # Изменяем размер, сохраняя пропорции
        im.thumbnail(max_size)

        # Сохраняем с оптимизацией
        im.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)

        return InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}.jpg",
                                    'image/jpeg', sys.getsizeof(output), None)
    return image


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    main_image = models.ImageField(upload_to='blog_images/',
                                   verbose_name='Главное изображение',
                                   validators=[validate_file_size])
    second_title = models.CharField(max_length=200,
                                    verbose_name='Второй заголовок')
    content = RichTextField(verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.main_image:
            self.main_image = compress_image(self.main_image)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class BlogSection(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='sections',
                                  on_delete=models.CASCADE,
                                  verbose_name='Публикация')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog_section_images/', blank=True,
                              null=True, verbose_name='Картинка',
                              validators=[validate_file_size])
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Раздел блога'
        verbose_name_plural = 'Разделы блога'

    def __str__(self):
        return f"Раздел: {self.title}"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)


def clear_unused_media():
    """Удаляет неиспользуемые медиа-файлы"""
    used_files = set()
    for blog_post in BlogPost.objects.all():
        if blog_post.main_image:
            used_files.add(blog_post.main_image.name)
    for blog_section in BlogSection.objects.all():
        if blog_section.image:
            used_files.add(blog_section.image.name)

    media_root = settings.MEDIA_ROOT
    for root, dirs, files in os.walk(media_root):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, media_root)
            if relative_path not in used_files:
                os.remove(file_path)


def optimize_all_images():
    """Оптимизирует все существующие изображения"""
    for blog_post in BlogPost.objects.all():
        if blog_post.main_image:
            optimized_image = compress_image(blog_post.main_image)
            blog_post.main_image.save(blog_post.main_image.name, optimized_image, save=False)
            blog_post.save()

    for blog_section in BlogSection.objects.all():
        if blog_section.image:
            optimized_image = compress_image(blog_section.image)
            blog_section.image.save(blog_section.image.name, optimized_image, save=False)
            blog_section.save()