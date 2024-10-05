from django.db import models
from common.models import Comments, Inquiry, Tag, City, Country
from ckeditor.fields import RichTextField
from django.db.models import Avg


class FlightComments(Comments):
    flight = models.ForeignKey('Flight', on_delete=models.SET_NULL, null=True, related_name='comments', verbose_name='Отзывы')

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

    def __str__(self):
        return f'{self.title} ({self.from_city} -> {self.to_city})'

    class Meta:
        verbose_name = 'Авиаперелет'
        verbose_name_plural = 'Авиаперелеты'


class FlightImage(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='images', verbose_name='Рейс')
    image = models.ImageField(upload_to='flight_images/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Изображение авиаперелета'
        verbose_name_plural = 'Изображения авиаперелетов'


class FlightInquiry(Inquiry):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='inquiries', verbose_name='Запросы')

    def __str__(self):
        return f'Запрос от {self.full_name} ({self.phone})'

    class Meta:
        verbose_name = 'Запрос на информацию об авиаперелете'
        verbose_name_plural = 'Запросы на информацию об авиаперелетах'


class IconsAfterName(models.Model):
    icon_city_country = models.FileField(verbose_name='Иконка для "Откуда/Куда"')
    icon_date = models.FileField(verbose_name='Иконка для даты "Туда/Обратно"')

    class Meta:
        verbose_name = 'Иконка после названия'
        verbose_name_plural = 'Иконки после названия'
