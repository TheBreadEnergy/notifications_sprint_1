import os

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

DEBUG = os.environ.get("DEBUG", "False") == "True"
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

INSTALLED_APPS += ["movies", "rest_framework"]
