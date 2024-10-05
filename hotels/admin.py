from django.contrib import admin
from .models import Hotel, HotelImage, HotelComments, HotelInquiry, IconsAfterName


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'get_final_rating', 'rating_count', 'is_popular_hotel']
    list_editable = ['is_popular_hotel']
    inlines = [HotelImageInline]
    readonly_fields = ['average_rating', 'rating_count']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_rating()
        self._update_popular_hotels(obj)

    def _update_popular_hotels(self, hotel):
        from main.models import PopularHotel
        popular_hotel, _ = PopularHotel.objects.get_or_create(id=1)
        if hotel.is_popular_hotel:
            popular_hotel.hotels.add(hotel)
        else:
            popular_hotel.hotels.remove(hotel)

    def get_final_rating(self, obj):
        return obj.get_final_rating()

    get_final_rating.short_description = 'Рейтинг'


@admin.register(HotelComments)
class HotelCommentsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'hotel', 'rate', 'date', 'is_approved']
    list_filter = ['is_approved', 'date', 'rate']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        for comment in queryset:
            if comment.hotel:
                comment.hotel.update_rating()

    approve_comments.short_description = "Одобрить выбранные отзывы"


@admin.register(HotelInquiry)
class HotelInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'hotel', 'created_at']
    list_filter = ['created_at', 'hotel']
    search_fields = ['name', 'phone_number', 'email']
    readonly_fields = ['created_at']


@admin.register(IconsAfterName)
class IconsAfterNameAdmin(admin.ModelAdmin):
    list_display = ['icon_city_country', 'icon_location']