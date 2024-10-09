from modeltranslation.translator import translator, TranslationOptions
from .models import BlogPost, BlogSection


class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'second_title', 'content')


translator.register(BlogPost, BlogPostTranslationOptions)


class BlogSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(BlogSection, BlogSectionTranslationOptions)
