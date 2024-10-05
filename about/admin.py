from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms


@admin.register(AboutUsConsultant)
class AboutUsConsultantAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone_number', 'is_active')
    list_editable = ('is_active',)

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            """Снять активность с других консультантов"""
            AboutUsConsultant.objects.filter(is_active=True).exclude(pk=obj.pk).update(is_active=False)

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Чтобы показывать всех консультантов в правильном порядке"""
        queryset = super().get_queryset(request)
        return queryset.order_by('-is_active', 'name')


@admin.register(AboutUsInquiry)
class AboutUsInquiryAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['phone_number']
    readonly_fields = ['created_at']


class AboutUsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label='Описание')

    class Meta:
        model = AboutUs
        fields = '__all__'


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsAdminForm
    list_display = ('title', 'youtube_video_url')
    search_fields = ('title',)
    list_editable = ('youtube_video_url',)


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
    list_display = ('question', 'order')
    list_editable = ('order',)
    ordering = ('order',)

    def save_model(self, request, obj, form, change):
        if not change and FAQ.objects.count() >= 8:
            messages.error(request, "Максимум можно добавить 8 изображений.")
            return
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if FAQ.objects.count() >= 8:
            return False
        return super().has_add_permission(request)


@admin.register(OurProjects)
class OurProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_video_url')
    filter_horizontal = ('tours',)

    def has_add_permission(self, request):
        return not OurProjects.objects.exists()




