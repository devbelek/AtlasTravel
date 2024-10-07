from django.db import models
from django.utils.html import format_html
from ckeditor.fields import RichTextField


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
    rent_of_car = models.ForeignKey(RentOfCar, related_name='images', on_delete=models.CASCADE, verbose_name='Аренда автомобиля')
    image = models.ImageField(upload_to='car_rentals/', verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Изображение аренды автомобиля"
        verbose_name_plural = "Изображения аренды автомобилей"
        ordering = ['order']

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="auto" />', self.image.url)
        return "-"

    image_tag.short_description = 'Превью'


class RentOfCarDescription(models.Model):
    rent_of_car = models.ForeignKey(RentOfCar, related_name='descriptions', on_delete=models.CASCADE, verbose_name='Аренда автомобиля')
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

    class Meta:
        verbose_name = "Преимущество работы с нами"
        verbose_name_plural = "Преимущества работы с нами"
