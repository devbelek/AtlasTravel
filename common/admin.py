from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Country, City, Tag, Comments, Inquiry


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fieldsets = (
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


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    fieldsets = (
        ('Страна', {
            'fields': ('country',),
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
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'rate', 'date', 'is_approved')
    list_filter = ('is_approved', 'date')
    search_fields = ('full_name', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Одобрить выбранные отзывы'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    pass
