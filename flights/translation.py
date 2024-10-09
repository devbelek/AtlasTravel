from modeltranslation.translator import translator, TranslationOptions
from .models import Flight


class FlightTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Flight, FlightTranslationOptions)