from modeltranslation.translator import translator, TranslationOptions
from .models import (AboutUs, AboutUsImage, FAQ,
                     OurProjects, PrivacyPolicy, UserAgreement, ReturnPolicy)


class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(AboutUs, AboutUsTranslationOptions)


class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


translator.register(FAQ, FAQTranslationOptions)


class OurProjectsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(OurProjects, OurProjectsTranslationOptions)


class PrivacyPolicyTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(PrivacyPolicy, PrivacyPolicyTranslationOptions)


class UserAgreementTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(UserAgreement, UserAgreementTranslationOptions)


class ReturnPolicyTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(ReturnPolicy, ReturnPolicyTranslationOptions)
