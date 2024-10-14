import asyncio
from django.core.management.base import BaseCommand
from telegram_bot import bot


class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))

        # Запуск асинхронного приложения
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot_application.start())