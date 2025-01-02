from django.contrib.auth.models import User
from django.db import models


# we use User.username field for storing unique UUID because this field is mandatory,
# and we don't have any other information about the user on the creation step
class CustomUser(User):
    telegram_username = models.CharField(max_length=32, unique=True, null=True)
    # Unique user id from telegram
    telegram_id = models.IntegerField(unique=True, editable=False, null=True)
    # UUID of existing user with given telegram_id
    parent_username = models.UUIDField(editable=False, null=True)
