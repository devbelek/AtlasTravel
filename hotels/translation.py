from modeltranslation.translator import translator, TranslationOptions
from .models import Hotel


class HotelTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Hotel, HotelTranslationOptions)
