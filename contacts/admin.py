from django.contrib import admin
from .models import Contacts


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ['title', 'formatted_phone_number', 'job', 'mail', 'address']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'job', 'phone_number', 'mail', 'address')
        }),
    )
    readonly_fields = ['formatted_phone_number']

    def formatted_phone_number(self, obj):
        return obj.formatted_phone_number()

    formatted_phone_number.short_description = 'Номер телефона (форматированный)'
