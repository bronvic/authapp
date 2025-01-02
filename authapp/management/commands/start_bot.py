from django.core.management.base import BaseCommand

from bot.bot import Command as BotCommand


class Command(BaseCommand):
    help = "Запуск Telegram бота"

    def handle(self, *args, **kwargs):
        bot_command = BotCommand()
        bot_command.handle()
