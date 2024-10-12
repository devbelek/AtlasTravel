from modeltranslation.translator import translator, TranslationOptions
from .models import Tag, Comments, Country


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Tag, TagTranslationOptions)


class CommentsTranslationOptions(TranslationOptions):
    fields = ('text', )


translator.register(Comments, CommentsTranslationOptions)


class CountryTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(Country, CountryTranslationOptions)
