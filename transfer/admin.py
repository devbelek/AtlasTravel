from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from ckeditor.widgets import CKEditorWidget
from .models import Transfer, TransferImage, TransferComments, TransferInquiry, IconsAfterName


class TransferAdminForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TransferAdminForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.LANGUAGES:
            description_field = 'description_%s' % lang_code
            if description_field in self.fields:
                self.fields[description_field].widget = CKEditorWidget(config_name='default')
            title_field = 'title_%s' % lang_code
            if title_field in self.fields:
                self.fields[title_field].widget = forms.TextInput()


class TransferImageInline(TabularInline):
    max_num = 15
    extra = 1
    model = TransferImage


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    form = TransferAdminForm
    inlines = [TransferImageInline]
    list_display = ['title_ru', 'city', 'departure_date', 'return_date', 'passengers', 'get_final_rating', 'rating_count']
    list_filter = ['city', 'departure_date', 'return_date']
    search_fields = ['title_ky', 'title_ru', 'title_en', 'description_ky', 'description_ru', 'description_en']
    readonly_fields = ['average_rating', 'rating_count']

    fieldsets = (
        ('Основная информация', {
            'fields': ('city', 'departure_date', 'return_date', 'passengers', 'tags')
        }),
        ('Кыргызский', {
            'fields': ('title_ky', 'description_ky'),
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru'),
        }),
        ('Английский', {
            'fields': ('title_en', 'description_en'),
        }),
        ('Рейтинг', {
            'fields': ('manual_rating', 'average_rating', 'rating_count')
        }),
    )

    def get_final_rating(self, obj):
        return obj.get_final_rating()
    get_final_rating.short_description = 'Рейтинг'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_rating()


@admin.register(TransferComments)
class TransferCommentsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'transfer', 'rate', 'date', 'is_approved']
    list_filter = ['is_approved', 'date', 'rate']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        for comment in queryset:
            if comment.transfer:
                comment.transfer.update_rating()

    approve_comments.short_description = "Одобрить выбранные отзывы"


@admin.register(TransferInquiry)
class TransferInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'created_at', 'transfer']
    list_filter = ['created_at', 'transfer']
    search_fields = ['name', 'phone_number', 'email']
    readonly_fields = ['created_at']


@admin.register(IconsAfterName)
class IconsAfterNameAdmin(admin.ModelAdmin):
    list_display = ['icon_city_country', 'icon_location']
