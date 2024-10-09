from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import BlogPost, BlogSection


class BlogSectionInline(SortableInlineAdminMixin, TranslationTabularInline):
    model = BlogSection
    extra = 1
    fieldsets = (
        ('Основное', {
            'fields': ('image', 'image_preview', 'order'),
        }),
        ('Кыргызский', {
            'fields': ('title_ky', 'content_ky'),
        }),
        ('Русский', {
            'fields': ('title_ru', 'content_ru'),
        }),
        ('Английский', {
            'fields': ('title_en', 'content_en'),
        }),
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; '
                               'max-width: 100%;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Предпросмотр изображения'


@admin.register(BlogPost)
class BlogPostAdmin(SortableAdminBase, TranslationAdmin):
    list_display = ('title', 'main_image_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('main_image', 'main_image_preview', 'created_at', 'updated_at')
        }),
        ('Кыргызский', {
            'fields': ('title_ky', 'second_title_ky', 'content_ky'),
        }),
        ('Русский', {
            'fields': ('title_ru', 'second_title_ru', 'content_ru'),
        }),
        ('Английский', {
            'fields': ('title_en', 'second_title_en', 'content_en'),
        }),
    )
    readonly_fields = ('main_image_preview', 'created_at', 'updated_at')
    inlines = [BlogSectionInline]

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 200px; '
                               'max-width: 100%;" />', obj.main_image.url)
        return "Нет изображения"

    main_image_preview.short_description = 'Предпросмотр главного изображения'
