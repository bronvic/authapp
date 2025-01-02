import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from authapp.models import CustomUser as User

logger = logging.getLogger("authapp")


class Command(BaseCommand):
    help = "Delete all users with active=False and date_joined more than 1 day ago"

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=1)

        inactive_users = User.objects.filter(
            is_active=False, date_joined__lt=cutoff_date
        )

        count = inactive_users.count()
        inactive_users.delete()

        logger.info(
            f"Deleted {count} users with is_active=False and date_joined more than 1 day ago"
        )
