import asyncio
from django.core.management.base import BaseCommand
from telegram_bot.bot import main  # Импортируем функцию main, которая запускает бота


class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
        asyncio.run(main())  # Запускаем асинхронную функцию main