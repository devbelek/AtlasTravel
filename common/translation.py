from modeltranslation.translator import translator, TranslationOptions
from .models import Tag, Comments


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Tag, TagTranslationOptions)


class CommentsTranslationOptions(TranslationOptions):
    fields = ('full_name', 'text')


translator.register(Comments, CommentsTranslationOptions)
