from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Country, City, Tag, Comments, Inquiry


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ('name', 'icon')

    fieldsets = (
        ('Основная информация', {
            'fields': ('icon', )
        }),
        ('Кыргызский', {
            'fields': ('name_ky', ),
        }),
        ('Русский', {
            'fields': ('name_ru', ),
        }),
        ('Английский', {
            'fields': ('name_en', ),
        }),
    )


@admin.register(Comments)
class CommentsAdmin(TranslationAdmin):
    list_display = ('full_name', 'rate', 'date', 'is_approved')
    list_filter = ('is_approved', 'date')
    search_fields = ('full_name', 'text')
    actions = ['approve_comments']

    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'rate', 'is_approved')
        }),
        ('Кыргызский', {
            'fields': ('text_ky', ),
        }),
        ('Русский', {
            'fields': ('text_ru', ),
        }),
        ('Английский', {
            'fields': ('text_en', ),
        }),
    )

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Одобрить выбранные отзывы'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    pass
