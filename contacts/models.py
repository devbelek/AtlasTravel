from django.db import models
from ckeditor.fields import RichTextField


class Contacts(models.Model):
    title = models.CharField(max_length=50, default='Контакты', verbose_name='Заголовок')
    description = RichTextField(verbose_name='Описание')
    job = models.CharField(max_length=200, verbose_name='Режим работы')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Почта')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    whatsapp = models.URLField(verbose_name='WhatsApp', blank=True, null=True)
    telegram = models.URLField(verbose_name='Telegram', blank=True, null=True)
    instagram = models.URLField(verbose_name='Instagram', blank=True, null=True)
    tiktok = models.URLField(verbose_name='TikTok', blank=True, null=True)
    facebook = models.URLField(verbose_name='Facebook', blank=True, null=True)
    youtube = models.URLField(verbose_name='YouTube', blank=True, null=True)

    def formatted_phone_number(self):
        if len(self.phone_number) == 12 and self.phone_number.startswith("+996"):
            return f"{self.phone_number[:4]} {self.phone_number[4:7]} {self.phone_number[7:9]} {self.phone_number[9:]}"
        return self.phone_number

    formatted_phone_number.short_description = 'Номер телефона (форматированный)'

    def __str__(self):
        return f'{self.title} - {self.formatted_phone_number()}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
