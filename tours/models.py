from django.db import models
from django.db.models import Avg


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
    tour = models.ForeignKey('Tour', on_delete=models.SET_NULL, null=True, related_name='comments', verbose_name='Отзывы')
    is_approved = models.BooleanField(default=False, verbose_name='Прошёл модерацию')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.tour:
            self.tour.update_rating()

    def __str__(self):
        return f'{self.full_name} {self.rate}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


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


class Tour(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    start_tour = models.DateField(verbose_name='Начало сезона')
    end_tour = models.DateField(verbose_name='Конец сезона')
    tags = models.ManyToManyField(Tag, related_name='tours', verbose_name='Теги')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='tours_from', verbose_name='Откуда')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='tours_to', verbose_name='Куда')
    departure_date = models.DateField(verbose_name='Дата вылета')
    nights = models.PositiveIntegerField(verbose_name='Количество ночей')

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
        return f'{self.title} {self.start_tour} {self.end_tour}'

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images', verbose_name='Тур')
    image = models.ImageField(upload_to='tour_images/', verbose_name='Фото')


class Inquiry(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    message = models.TextField(verbose_name="Сообщение", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    tour = models.ForeignKey('Tour', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тур', related_name='inquiries')

    def __str__(self):
        return f'{self.name} - {self.phone_number}'

    class Meta:
        verbose_name = 'Запрос на информацию'
        verbose_name_plural = 'Запросы на информацию'
