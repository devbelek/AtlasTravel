from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Страна', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = False
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Город')
    country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Страна')

    def __str__(self):
        return self.name

    class Meta:
        abstract = False
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Tag(models.Model):
    icon = models.FileField(verbose_name='Иконка')
    name = models.CharField(max_length=30, verbose_name='Тег', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = False
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Inquiry(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    message = models.TextField(verbose_name="Сообщение", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.name} - {self.phone_number}'

    class Meta:
        abstract = False
        verbose_name = 'Запрос на информацию'
        verbose_name_plural = 'Запросы на информацию'


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
    is_approved = models.BooleanField(default=False, verbose_name='Прошёл модерацию')

    def __str__(self):
        return f'{self.full_name} {self.rate}'

    class Meta:
        abstract = False
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

