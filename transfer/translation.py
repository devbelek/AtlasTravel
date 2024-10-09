from modeltranslation.translator import translator, TranslationOptions
from .models import Transfer


class TransferTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Transfer, TransferTranslationOptions)
