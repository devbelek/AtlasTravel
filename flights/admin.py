from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin

from .models import Flight, FlightImage, FlightComments, FlightInquiry, IconsAfterName


class FlightAdminForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for lang_code, lang_name in settings.LANGUAGES:
            description_field = 'description_%s' % lang_code
            if description_field in self.fields:
                self.fields[description_field].widget = CKEditorWidget(config_name='default')
            title_field = 'title_%s' % lang_code
            if title_field in self.fields:
                self.fields[title_field].widget = forms.TextInput()


@admin.register(FlightComments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'flight', 'rate', 'date', 'is_approved']
    list_filter = ['is_approved', 'date', 'rate']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        for comment in queryset:
            if comment.flight:
                comment.flight.update_rating()

    approve_comments.short_description = "Одобрить выбранные отзывы"


class FlightImageInline(TabularInline):
    max_num = 15
    extra = 1
    model = FlightImage


@admin.register(Flight)
class FlightAdmin(TranslationAdmin):
    form = FlightAdminForm
    inlines = [FlightImageInline]
    list_display = ['title', 'departure_date', 'return_date', 'get_final_rating', 'rating_count']
    readonly_fields = ['average_rating', 'rating_count']

    fieldsets = (
        ('Основная информация', {
            'fields': ('from_city', 'to_city', 'departure_date', 'return_date', 'passengers', 'class_type', 'tags')
        }),
        ('Рейтинг', {
            'fields': ('manual_rating', 'average_rating', 'rating_count')
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
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


    def get_final_rating(self, obj):
        return obj.get_final_rating()

    get_final_rating.short_description = 'Рейтинг'


@admin.register(FlightInquiry)
class FlightInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'flight', 'created_at']
    list_filter = ['created_at', 'flight']
    search_fields = ['name', 'phone_number', 'email']
    readonly_fields = ['created_at']


@admin.register(IconsAfterName)
class IconsAfterNameAdmin(admin.ModelAdmin):
    list_display = ['icon_city_country', 'icon_date']
