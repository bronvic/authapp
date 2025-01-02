import logging
import os
import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import generics

from authapp.models import CustomUser as User
from authapp.serializers import UserSerializer

TELEGRAM_BOT_NAME = os.environ.get("BOT_NAME")


logger = logging.getLogger("authapp")


def home_view(request: HttpRequest) -> HttpResponse:
    username = str(uuid.uuid4())
    telegram_login_url = f"https://t.me/{TELEGRAM_BOT_NAME}?start={username}"
    logger.info(f"New user with uuid {username} is going to be created")
    return render(
        request,
        "home.html",
        {"telegram_login_url": telegram_login_url, "username": username},
    )


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self) -> User:
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)
