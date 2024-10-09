from modeltranslation.translator import translator, TranslationOptions
from .models import Contacts


class ContactsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'job')


translator.register(Contacts, ContactsTranslationOptions)
