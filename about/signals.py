from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AboutUsInquiry, AboutUsConsultant
from telegram_bot.utils import send_about_us_notification


@receiver(post_save, sender=AboutUsInquiry)
def about_us_inquiry_post_save(sender, instance, created, **kwargs):
    if created:
        send_about_us_notification(instance)