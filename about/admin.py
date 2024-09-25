from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin

from .models import *


class AboutUsImageInline(TabularInline):
    max_num = 15
    extra = 1
    model = AboutUsImage


@admin.register(AboutUs)
class AboutUsAdmin(ModelAdmin):
    inlines = [AboutUsImageInline]
    list_display = ['title', 'description']


