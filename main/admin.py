from django.contrib import admin
from .models import RestIdea, BestChoice, PopularHotel, RentOfCar, RentOfCarDescription, Benefits, RentOfCarImage


@admin.register(RestIdea)
class RestIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_tours']
    filter_horizontal = ('tours',)

    def get_tours(self, obj):
        return ", ".join([f"{tour.title_ru} ({tour.start_tour} - {tour.end_tour})" for tour in obj.tours.all()])

    get_tours.short_description = 'Туры'


@admin.register(BestChoice)
class BestChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_tours']
    filter_horizontal = ('tours',)

    def get_tours(self, obj):
        return ", ".join([f"{tour.title_ru} ({tour.start_tour} - {tour.end_tour})" for tour in obj.tours.all()])

    get_tours.short_description = 'Туры'


@admin.register(PopularHotel)
class PopularHotelAdmin(admin.ModelAdmin):
    list_display = ['get_hotels']
    filter_horizontal = ('hotels',)

    def get_hotels(self, obj):
        return ", ".join([f"{hotel.title_ru} ({hotel.description_ru} - {hotel.city})" for hotel in obj.hotels.all()])

    get_hotels.short_description = 'Отели'


class RentOfCarImageInline(admin.TabularInline):
    model = RentOfCarImage
    extra = 1
    fields = ('image', 'order', 'image_tag')
    readonly_fields = ('image_tag',)


class RentOfCarDescriptionInline(admin.TabularInline):
    model = RentOfCarDescription
    extra = 1
    fields = ('description_ky', 'description_ru', 'description_en', 'order')


@admin.register(RentOfCar)
class RentOfCarAdmin(admin.ModelAdmin):
    list_display = ['title_ru']
    inlines = [RentOfCarImageInline, RentOfCarDescriptionInline]
    fieldsets = (
        ('Кыргызский', {
            'fields': ('title_ky',),
        }),
        ('Русский', {
            'fields': ('title_ru',),
        }),
        ('Английский', {
            'fields': ('title_en',),
        }),
    )


@admin.register(Benefits)
class BenefitsAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title_ru')
    fieldsets = (
        ('Общее', {
            'fields': ('icon',),
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