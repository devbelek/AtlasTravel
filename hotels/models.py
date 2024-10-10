from django.db import models
from common.models import Comments, Inquiry, Tag, City, Country
from ckeditor.fields import RichTextField
from django.db.models import Avg, Q
from PIL import Image
from io import BytesIO
from django.core.files import File
import os


class HotelComments(Comments):
    hotel = models.ForeignKey('Hotel', on_delete=models.SET_NULL, null=True, related_name='comments', verbose_name='Отзывы')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.hotel:
            self.hotel.update_rating()

    class Meta:
        verbose_name = 'Отзыв об отеле'
        verbose_name_plural = 'Отзывы об отелях'


class Hotel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название отеля')
    description = RichTextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag, related_name='hotels', verbose_name='Теги')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels_from', verbose_name='Город')
    arrival_date = models.DateField(verbose_name='Дата заезда')
    departure_date = models.DateField(verbose_name='Дата выезда')
    nights = models.PositiveIntegerField(verbose_name='Количество ночей')

    manual_rating = models.FloatField(default=None, null=True, blank=True, verbose_name='Ручной рейтинг')
    average_rating = models.FloatField(default=0, verbose_name='Средний рейтинг')
    rating_count = models.PositiveIntegerField(default=0, verbose_name='Количество оценок')

    is_popular_hotel = models.BooleanField(default=False, verbose_name='Популярный отель')

    def update_rating(self):
        comments = self.comments.filter(is_approved=True)
        self.rating_count = comments.count()
        self.average_rating = (comments.aggregate(Avg('rate'))['rate__avg'] or 0) * 2
        self.save()

    def get_final_rating(self):
        return self.manual_rating if self.manual_rating is not None else self.average_rating

    def find_similar_hotels(self, limit=3):
        return Hotel.objects.filter(
            Q(city=self.city) |
            Q(nights__range=(self.nights - 2, self.nights + 2)) |
            Q(tags__in=self.tags.all())
        ).exclude(id=self.id).distinct().order_by('-average_rating')[:limit]

    def __str__(self):
        return f'{self.title} {self.city}'

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class PopularHotels(Hotel):
    class Meta:
        proxy = True
        verbose_name = 'Популярный отель'
        verbose_name_plural = 'Популярные отели'


class HotelImage(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='images', verbose_name='Отель')
    image = models.ImageField(upload_to='hotel_images/', verbose_name='Фото')

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


class HotelInquiry(Inquiry):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='inquiries', verbose_name='Отель')

    def __str__(self):
        return f'Запрос от {self.name} по отелю {self.hotel.title}'

    class Meta:
        verbose_name = 'Запрос на информацию об отеле'
        verbose_name_plural = 'Запросы на информацию об отелях'


class IconsAfterName(models.Model):
    icon_city_country = models.FileField(verbose_name='Иконка для "Страна/Город"')

    location_text = models.CharField(max_length=30, verbose_name='Находится в центре', default='Находится в центре')
    icon_location = models.FileField(verbose_name='Иконка для "Местоположения(Находится в центре)"')

    class Meta:
        verbose_name = 'Иконка после названия'
        verbose_name_plural = 'Иконки после названия'
