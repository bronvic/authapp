import logging
import os

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from authapp.exceptions import MissingUserUUIDError
from authapp.models import CustomUser as User

logger = logging.getLogger("myapp")


BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set")
    raise ValueError("BOT_TOKEN must be set in the environment variables")


class Command(BaseCommand):
    help = "Telegram bot start"

    def handle(self, *args, **kwargs):
        application = ApplicationBuilder().token(BOT_TOKEN).build()

        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if not context.args:
                logger.warning("Start command triggered without UUID")
                raise MissingUserUUIDError("User UUID is missing")

            # UUID of user provided by API call
            supposed_username = context.args[0]
            first_name = update.message.from_user.first_name
            last_name = update.message.from_user.last_name or ""
            telegram_username = update.message.from_user.username
            telegram_id = update.message.from_user.id

            user = await self.get_user(supposed_username)
            await self.activate_existing_user(
                user, telegram_id, first_name, last_name, telegram_username
            )

            await update.message.reply_text(
                f"Привет, {first_name}{' ' + last_name if last_name else ''}! Ты успешно авторизован\n"
            )

        application.add_handler(CommandHandler("start", start))
        application.run_polling()

    async def get_user(self, username: str) -> User:
        return await sync_to_async(User.objects.get)(username=username)

    async def activate_existing_user(
        self,
        user: User,
        telegram_id: int,
        first_name: str,
        last_name: str,
        telegram_username: str,
    ) -> None:
        try:
            # if we have parent user that means that this user have been registered before
            # we need to change parent_username of our current user
            # to let API know that it should poll previous user with username=parent_id
            parent_user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
            user.parent_username = parent_user.username
            logger.info(
                f"{user.username} has been activated before as {parent_user.username}"
            )
        except User.DoesNotExist:
            # if parent user does not exist that means that this is the first time when user login to the system
            # in that case we just mark user as active and fill all their fields
            logger.info(f"{user.username} is a new user.")
            user.first_name = first_name
            user.last_name = last_name
            user.telegram_username = telegram_username
            user.telegram_id = telegram_id
            user.is_active = True
        await sync_to_async(user.save)()
