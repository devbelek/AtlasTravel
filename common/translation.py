from modeltranslation.translator import translator, TranslationOptions
from .models import Tag, Comments, Country, City


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Tag, TagTranslationOptions)


class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(City, CityTranslationOptions)


class CountryTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(Country, CountryTranslationOptions)
