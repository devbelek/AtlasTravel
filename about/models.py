from django.db import models


class AboutUs(models.Model):
    title = models.CharField(max_length=200, verbose_name='О нас')
    description = models.TextField(verbose_name='Описание')
    # our_projects = models.

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'


class AboutUsImage(models.Model):
    about = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name='image', verbose_name='О нас')
    image = models.ImageField(upload_to='about_images/', verbose_name='Картинка')

    def __str__(self):
        return f'{self.about}'

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
