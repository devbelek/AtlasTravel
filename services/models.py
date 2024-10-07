from django.db import models
from ckeditor.fields import RichTextField


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

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение услуги'
        verbose_name_plural = 'Изображения услуг'

    def __str__(self):
        return f"Изображение: {self.service.title}, Главное: {'Да' if self.is_main else 'Нет'}"


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