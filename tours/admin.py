from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import *
from django.contrib.auth.models import Group, User

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Tag)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'tour', 'rate', 'date', 'is_approved']
    list_filter = ['is_approved', 'date', 'rate']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        for comment in queryset:
            if comment.tour:
                comment.tour.update_rating()

    approve_comments.short_description = "Одобрить выбранные отзывы"


class TourImageInline(TabularInline):
    max_num = 15
    extra = 1
    model = TourImage


@admin.register(Tour)
class TourAdmin(ModelAdmin):
    inlines = [TourImageInline]
    list_display = ['title', 'start_tour', 'end_tour', 'get_final_rating', 'rating_count']
    readonly_fields = ['average_rating', 'rating_count']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_rating()

    def get_final_rating(self, obj):
        return obj.get_final_rating()

    get_final_rating.short_description = 'Рейтинг'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'created_at', 'tour']
    list_filter = ['created_at', 'tour']
    search_fields = ['name', 'phone_number', 'email']
    readonly_fields = ['created_at']






