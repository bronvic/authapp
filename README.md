# Django Telegram Authentication Project

## Description
This project implements a Django web application that allows users to authenticate using a Telegram bot. The application provides a seamless login experience by redirecting users to a Telegram bot, where they can initiate the authentication process. Upon successful authentication, the user's Telegram account is linked to their web account, and their name is displayed on the web page

## Requirements
* Python 3.x
* Poetry
* Django
* Djangorestframework
* Requests
* Python-telegram-bot
* Docker 
* Docker Compose

## Setup

### Environment Variables
Before running the application, make sure to set the following environment variables in a .env file or your environment:

* `DJANGO_SECRET_KEY`: A secret key for your Django application.
* `DJANGO_DEBUG`: Set to `True` for development, `False` for production.
* `BOT_NAME`: The name of your Telegram bot.
* `BOT_TOKEN`: The token for your Telegram bot.

### Running the Application
1. Clone the repository:
```commandline
git clone <repository-url>
cd <repository-directory>
```
2. Build and run the Docker containers:
```commandline
docker-compose up --build
```

## Usage
1. On the web page, click the "Login with Telegram" button.
2. You will be redirected to the Telegram bot, where a command /start will be sent with a unique token.
3. After sending the command, the Django application will receive the token and link your Telegram account with your web account.
4. The web page will refresh, displaying your name from Telegram.

### Delete inactive users
In order to keep database clean, you should run `clean_inactive_users` command. The command deletes all user which has `is_active=False` and `date_joined` more than 1 day ago
```commandline
python manage.py clean_inactive_users
```

## License
This project is licensed under the [MIT License](https://github.com/bronvic/authapp/blob/main/LICENSE)
