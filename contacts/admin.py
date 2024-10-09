from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Contacts


@admin.register(Contacts)
class ContactsAdmin(TranslationAdmin):
    list_display = ['title', 'formatted_phone_number', 'job', 'email', 'address']
    fieldsets = (
        ('Основная информация', {
            'fields': ('phone_number', 'email', 'address')
        }),
        ('Социальные сети', {
            'fields': ('whatsapp', 'telegram', 'instagram', 'tiktok', 'facebook', 'youtube')
        }),
        ('Кыргызский', {
            'fields': ('title_ky', 'description_ky', 'job_ky'),
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru', 'job_ru'),
        }),
        ('Английский', {
            'fields': ('title_en', 'description_en', 'job_en'),
        }),
    )
    readonly_fields = ['formatted_phone_number']
