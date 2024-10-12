from django.contrib import admin, messages
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.db import models
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (AboutUs, AboutUsImage, FAQ, AboutUsInquiry,
                     AboutUsConsultant, OurProjects, PrivacyPolicy,
                     UserAgreement, ReturnPolicy)
from django.utils.translation import gettext_lazy as _


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title_ky', 'title_ru', 'title_en', 'youtube_video_url')
    search_fields = ('title_ky', 'title_ru', 'title_en')
    list_editable = ('youtube_video_url',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    fieldsets = (
        ('Основные', {
            'fields': ('youtube_video_url',),
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
    #
    # '''Ограничение на добавление новой записи'''
    # def has_add_permission(self, request):
    #     if AboutUs.objects.exists():
    #         return False
    #     return super().has_add_permission(request)
    #
    # '''Ограничение на отображение только одной записи'''
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs[:1]


@admin.register(AboutUsImage)
class AboutUsImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'image_tag')
    list_editable = ('order',)
    ordering = ('order',)

    def save_model(self, request, obj, form, change):
        if not change and AboutUsImage.objects.count() >= 6:
            messages.error(request, "Максимум можно добавить 6 изображений.")
            return
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if AboutUsImage.objects.count() >= 6:
            return False
        return super().has_add_permission(request)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_ky', 'question_ru', 'question_en')
    fieldsets = (
        ('Кыргызский', {
            'fields': ('question_ky', 'answer_ky'),
        }),
        ('Русский', {
            'fields': ('question_ru', 'answer_ru'),
        }),
        ('Английский', {
            'fields': ('question_en', 'answer_en'),
        }),
    )


@admin.register(AboutUsInquiry)
class AboutUsInquiryAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['phone_number']
    readonly_fields = ['created_at']


@admin.register(AboutUsConsultant)
class AboutUsConsultantAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone_number', 'is_active')
    list_editable = ('is_active',)

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            AboutUsConsultant.objects.filter(is_active=True) \
                .exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-is_active', 'name')


@admin.register(OurProjects)
class OurProjectsAdmin(admin.ModelAdmin):
    list_display = ('title_ky', 'title_ru', 'title_en')
    fieldsets = (
        ('Основные', {
            'fields': ('tours', 'youtube_video_url'),
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
    filter_horizontal = ('tours',)

    def has_add_permission(self, request):
        return not OurProjects.objects.exists()


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_preview_ky', 'content_preview_ru', 'content_preview_en')
    search_fields = ('content_ky', 'content_ru', 'content_en')

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    fieldsets = (
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

    def content_preview_ky(self, obj):
        return (obj.content_ky[:100] + '...') if len(obj.content_ky) > 100 else obj.content_ky

    def content_preview_ru(self, obj):
        return (obj.content_ru[:100] + '...') if len(obj.content_ru) > 100 else obj.content_ru

    def content_preview_en(self, obj):
        return (obj.content_en[:100] + '...') if len(obj.content_en) > 100 else obj.content_en

    content_preview_ky.short_description = 'Content Preview (KY)'
    content_preview_ru.short_description = 'Content Preview (RU)'
    content_preview_en.short_description = 'Content Preview (EN)'


@admin.register(UserAgreement)
class UserAgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_preview_ky', 'content_preview_ru', 'content_preview_en')
    search_fields = ('content_ky', 'content_ru', 'content_en')

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    fieldsets = (
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

    def content_preview_ky(self, obj):
        return (obj.content_ky[:100] + '...') if len(obj.content_ky) > 100 else obj.content_ky

    def content_preview_ru(self, obj):
        return (obj.content_ru[:100] + '...') if len(obj.content_ru) > 100 else obj.content_ru

    def content_preview_en(self, obj):
        return (obj.content_en[:100] + '...') if len(obj.content_en) > 100 else obj.content_en

    content_preview_ky.short_description = 'Content Preview (KY)'
    content_preview_ru.short_description = 'Content Preview (RU)'
    content_preview_en.short_description = 'Content Preview (EN)'


@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_preview_ky', 'content_preview_ru', 'content_preview_en')
    search_fields = ('content_ky', 'content_ru', 'content_en')

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    fieldsets = (
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

    def content_preview_ky(self, obj):
        return (obj.content_ky[:100] + '...') if len(obj.content_ky) > 100 else obj.content_ky

    def content_preview_ru(self, obj):
        return (obj.content_ru[:100] + '...') if len(obj.content_ru) > 100 else obj.content_ru

    def content_preview_en(self, obj):
        return (obj.content_en[:100] + '...') if len(obj.content_en) > 100 else obj.content_en

    content_preview_ky.short_description = 'Content Preview (KY)'
    content_preview_ru.short_description = 'Content Preview (RU)'
    content_preview_en.short_description = 'Content Preview (EN)'
