from django.contrib import admin
from .models import VisaService, ServiceImage, ServiceFeature


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    ordering = ['order']
    fields = ['image', 'order', 'is_main']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_main:
            ServiceImage.objects.filter(service=obj.service, is_main=True).exclude(id=obj.id).update(is_main=False)


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    ordering = ['order']
    show_change_link = True
    can_delete = True
    fields = ['title_ru', 'description_ru', 'order']

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(VisaService)
class VisaServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceFeatureInline, ServiceImageInline]
    list_display = ['title_ru', 'created_at', 'updated_at']
    search_fields = ['title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en']
    fieldsets = (
        ('Кыргызский', {
            'fields': ('title_ky', 'subtitle_ky', 'description_ky'),
        }),
        ('Русский', {
            'fields': ('title_ru', 'subtitle_ru', 'description_ru'),
        }),
        ('Английский', {
            'fields': ('title_en', 'subtitle_en', 'description_en'),
        }),
    )


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'service', 'order']
    search_fields = ['title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en']
    fieldsets = (
        ('Кыргызский', {
            'fields': ('title_ky', 'description_ky'),
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru'),
        }),
        ('Английский', {
            'fields': ('title_en', 'description_en'),
        }),
        ('Другое', {
            'fields': ('service', 'order'),
        }),
    )