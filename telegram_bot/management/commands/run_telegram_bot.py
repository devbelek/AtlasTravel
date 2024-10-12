from django.core.management.base import BaseCommand
from telegram_bot.bot import bot_application


class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
        bot_application.run_polling()