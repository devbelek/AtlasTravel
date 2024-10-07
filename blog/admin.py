from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import BlogPost, BlogSection


class BlogSectionInline(SortableInlineAdminMixin, admin.StackedInline):
    model = BlogSection
    extra = 0
    fields = ('title', 'content', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 100%;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр изображения'


@admin.register(BlogPost)
class BlogPostAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'main_image_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'main_image', 'second_title', 'content', 'main_image_preview')
        }),
    )
    readonly_fields = ('main_image_preview',)
    inlines = [BlogSectionInline]

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 100%;" />', obj.main_image.url)
        return "Нет изображения"
    main_image_preview.short_description = 'Предпросмотр главного изображения'
