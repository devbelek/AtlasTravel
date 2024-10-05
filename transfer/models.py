from django.db import models
from common.models import Comments, Inquiry, Tag, City, Country
from ckeditor.fields import RichTextField
from django.db.models import Avg


class TransferComments(Comments):
    transfer = models.ForeignKey('Transfer', on_delete=models.SET_NULL, null=True, related_name='comments',
                                 verbose_name='Отзывы')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.transfer:
            self.transfer.update_rating()

    class Meta:
        verbose_name = 'Отзыв о трансфере'
        verbose_name_plural = 'Отзывы о трансферах'


class Transfer(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = RichTextField(verbose_name='Описание')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='transfer_city', verbose_name='Город')
    departure_date = models.DateField(verbose_name='Дата получения')
    return_date = models.DateField(verbose_name='Дата возврата')
    passengers = models.PositiveIntegerField(verbose_name='Количество пассажиров')
    tags = models.ManyToManyField(Tag, related_name='transfers', verbose_name='Теги')

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
        return f'{self.title} {self.city}'

    class Meta:
        verbose_name = 'Трансфер'
        verbose_name_plural = 'Трансферы'


class TransferImage(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='images', verbose_name='Трансфер')
    image = models.ImageField(upload_to='transfer_images/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Изображение трансфера'
        verbose_name_plural = 'Изображения трансферов'


class TransferInquiry(Inquiry):
    transfer = models.ForeignKey(Transfer, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries',
                                 verbose_name='Трансфер')

    class Meta:
        verbose_name = 'Запрос на информацию о трансфере'
        verbose_name_plural = 'Запросы на информацию о трансферах'


class IconsAfterName(models.Model):
    icon_city_country = models.FileField(verbose_name='Иконка для "Страна/Город"')

    location_text = models.CharField(max_length=30, verbose_name='Находится в центре', default='Находится в центре')
    icon_location = models.FileField(verbose_name='Иконка для "Местоположения(Находится в центре)"')

    class Meta:
        verbose_name = 'Иконка после названия'
        verbose_name_plural = 'Иконки после названия'
