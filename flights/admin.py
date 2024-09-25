from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import Flight, City, Country, Tag, FlightImage, Comments, Inquiry


admin.site.register(City)
admin.site.register(Country)
admin.site.register(Tag)


@admin.register(Comments)
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
class FlightAdmin(ModelAdmin):
    inlines = [FlightImageInline]
    list_display = ['title', 'departure_date', 'return_date', 'get_final_rating', 'rating_count']
    readonly_fields = ['average_rating', 'rating_count']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_rating()

    def get_final_rating(self, obj):
        return obj.get_final_rating()

    get_final_rating.short_description = 'Рейтинг'


@admin.register(Inquiry)
class InquiryAdmin(ModelAdmin):
    list_display = ['full_name', 'phone', 'email', 'flight']
