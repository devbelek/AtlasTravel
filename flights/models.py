from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import Comments, Inquiry, Tag, City, Country
from ckeditor.fields import RichTextField
from django.db.models import Avg, Q
from PIL import Image
from io import BytesIO
from django.core.files import File
import os
from telegram_bot.utils import send_review_notification, send_consultation_notification


class FlightComments(Comments):
    flight = models.ForeignKey('Flight', on_delete=models.SET_NULL, null=True, related_name='comments', verbose_name='Отзывы')
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.flight:
            self.flight.update_rating()

    class Meta:
        verbose_name = 'Отзыв на авиаперелет'
        verbose_name_plural = 'Отзывы на авиаперелеты'


class Flight(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название рейса')
    description = RichTextField(verbose_name='Описание')
    departure_date = models.DateField(verbose_name='Дата вылета')
    return_date = models.DateField(verbose_name='Дата возврата', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='flights', verbose_name='Теги')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='flights_from', verbose_name='Откуда')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='flights_to', verbose_name='Куда')
    passengers = models.PositiveIntegerField(verbose_name='Количество пассажиров')
    class_type = models.CharField(max_length=50, verbose_name='Класс обслуживания', choices=[
        ('economy', 'Эконом'), ('business', 'Бизнес')
    ])

    manual_rating = models.FloatField(default=None, null=True, blank=True, verbose_name='Ручной рейтинг')
    average_rating = models.FloatField(default=0, verbose_name='Средний рейтинг')
    rating_count = models.PositiveIntegerField(default=0, verbose_name='Количество оценок')

    def update_rating(self):
        comments = self.comments.filter(is_approved=True)
        self.rating_count = comments.count()
        self.average_rating = (comments.aggregate(Avg('rate'))['rate__avg'] or 0) * 2
        self.save()

    def get_final_rating(self):
        return self.manual_rating if self.manual_rating is not None else self.average_rating

    def find_similar_flights(self, limit=3):
        return Flight.objects.filter(
            Q(to_city=self.to_city) |
            Q(from_city=self.from_city) |
            Q(class_type=self.class_type) |
            Q(tags__in=self.tags.all())
        ).exclude(id=self.id).distinct().order_by('-average_rating')[:limit]

    def __str__(self):
        return f'{self.title} ({self.from_city} -> {self.to_city})'

    class Meta:
        verbose_name = 'Авиаперелет'
        verbose_name_plural = 'Авиаперелеты'


class FlightImage(models.Model):
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, related_name='images', verbose_name='Рейс')
    image = models.ImageField(upload_to='flight_images/', verbose_name='Фото')

    def compress_image(self):
        im = Image.open(self.image)
        if im.mode in ('RGBA', 'P'):
            im = im.convert('RGB')
        max_size = (800, 800)
        if im.size[0] > max_size[0] or im.size[1] > max_size[1]:
            im.thumbnail(max_size, Image.Resampling.LANCZOS)
        output = BytesIO()
        im.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        filename = os.path.splitext(os.path.basename(self.image.name))[0]
        self.image = File(output, name=f"{filename}_compressed.jpg")

    def save(self, *args, **kwargs):
        if self.image:
            self.compress_image()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class FlightInquiry(Inquiry):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='inquiries', verbose_name='Запросы')
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')

    def __str__(self):
        return f'{self.name} - {self.phone_number}'

    class Meta:
        verbose_name = 'Запрос на информацию об авиаперелете'
        verbose_name_plural = 'Запросы на информацию об авиаперелетах'


@receiver(post_save, sender=FlightComments)
def flight_comment_post_save(sender, instance, created, **kwargs):
    if created:
        from telegram_bot.utils import send_review_notification
        send_review_notification(instance)


@receiver(post_save, sender=FlightInquiry)
def flight_inquiry_post_save(sender, instance, created, **kwargs):
    if created:
        from telegram_bot.utils import send_consultation_notification
        send_consultation_notification(instance)


class IconsAfterName(models.Model):
    icon_city_country = models.FileField(verbose_name='Иконка для "Откуда/Куда"')
    icon_date = models.FileField(verbose_name='Иконка для даты "Туда/Обратно"')

    class Meta:
        verbose_name = 'Иконка после названия'
        verbose_name_plural = 'Иконки после названия'
