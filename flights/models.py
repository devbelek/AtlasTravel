from django.db import models
from django.db.models import Avg


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='Тег', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Страна')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Город')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Flight(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название рейса')
    description = models.TextField(verbose_name='Описание')
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


class Comments(models.Model):
    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, verbose_name='Оценка', null=True)
    full_name = models.CharField(max_length=100, verbose_name='Имя-Фамилия')
    text = models.CharField(max_length=200, verbose_name='Комментарий')
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, related_name='comments', verbose_name='Отзывы')
    is_approved = models.BooleanField(default=False, verbose_name='Прошёл модерацию')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.flight:
            self.flight.update_rating()

    def __str__(self):
        return f'{self.full_name} {self.rate}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Inquiry(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Имя-Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='inquiries', verbose_name='Запросы')

    def __str__(self):
        return f'Запрос от {self.full_name} ({self.phone})'

    class Meta:
        verbose_name = 'Запрос на информацию'
        verbose_name_plural = 'Запросы на информацию'
