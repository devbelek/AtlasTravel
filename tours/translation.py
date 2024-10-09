from modeltranslation.translator import translator, TranslationOptions
from .models import Tour


class TourTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Tour, TourTranslationOptions)
