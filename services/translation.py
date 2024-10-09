from modeltranslation.translator import register, TranslationOptions
from .models import VisaService, ServiceFeature


@register(VisaService)
class VisaServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description')


@register(ServiceFeature)
class ServiceFeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description')