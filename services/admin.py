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

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(VisaService)
class VisaServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceFeatureInline, ServiceImageInline]
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
