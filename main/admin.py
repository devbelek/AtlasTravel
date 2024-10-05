from django.contrib import admin
from .models import RestIdea, BestChoice, PopularHotel, RentOfCar, RentOfCarDescription, Benefits
from django.contrib import messages
from .models import RentOfCar, RentOfCarImage


@admin.register(RestIdea)
class RestIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_tours']
    filter_horizontal = ('tours',)

    def get_tours(self, obj):
        return ", ".join([f"{tour.title} ({tour.start_tour} - {tour.end_tour})" for tour in obj.tours.all()])

    get_tours.short_description = 'Туры'


@admin.register(BestChoice)
class BestChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_tours']
    filter_horizontal = ('tours',)

    def get_tours(self, obj):
        return ", ".join([f"{tour.title} ({tour.start_tour} - {tour.end_tour})" for tour in obj.tours.all()])

    get_tours.short_description = 'Туры'


@admin.register(PopularHotel)
class PopularHotelAdmin(admin.ModelAdmin):
    list_display = ['get_hotels']
    filter_horizontal = ('hotels',)

    def get_hotels(self, obj):
        return ", ".join([f"{hotel.title} ({hotel.description} - {hotel.from_city})" for hotel in obj.hotels.all()])

    get_hotels.short_description = 'Отели'


class RentOfCarImageInline(admin.TabularInline):
    model = RentOfCarImage
    extra = 1
    fields = ('image', 'order', 'image_tag')
    readonly_fields = ('image_tag',)


class RentOfCarDescriptionInline(admin.TabularInline):
    model = RentOfCarDescription
    extra = 1


@admin.register(RentOfCar)
class RentOfCarAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [RentOfCarImageInline, RentOfCarDescriptionInline]


@admin.register(RentOfCarImage)
class RentOfCarImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'rent_of_car', 'order', 'image_tag')
    list_editable = ('order',)
    ordering = ('rent_of_car', 'order')


@admin.register(RentOfCarDescription)
class RentOfCarDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'rent_of_car', 'description', 'order')
    list_editable = ('order',)
    ordering = ('rent_of_car', 'order')


@admin.register(Benefits)
class BenefitsAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'description')