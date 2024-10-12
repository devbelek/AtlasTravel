from django.core.management.base import BaseCommand
from telegram_bot.bot import bot_application


class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Запуск Telegram бота...'))
        bot_application.run_polling()