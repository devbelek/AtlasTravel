from django.db import models
from ckeditor.fields import RichTextField


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    main_image = models.ImageField(upload_to='blog_images/',
                                   verbose_name='Главное изображение')
    second_title = models.CharField(max_length=200,
                                    verbose_name='Второй заголовок')
    content = RichTextField(verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class BlogSection(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='sections',
                                  on_delete=models.CASCADE,
                                  verbose_name='Публикация')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog_section_images/', blank=True,
                              null=True, verbose_name='Картинка')
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Раздел блога'
        verbose_name_plural = 'Разделы блога'

    def __str__(self):
        return f"Раздел: {self.title}"
