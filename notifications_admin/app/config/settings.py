import os
from pathlib import Path

import backoff
from dotenv import load_dotenv
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DEBUG", "False") == "True"

if DEBUG:
    load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")


AUTH_API_LOGIN_URL = os.environ.get("AUTH_API_LOGIN_URL")
AUTH_API_PROFILE_URL = os.environ.get("AUTH_API_PROFILE_URL")

NOTIFICATION_SERVICE_GRPC = os.environ.get("NOTIFICATION_SERVICE_GRPC")

BACKOFF_MAX_RETRIES = os.environ.get("BACKOFF_MAX_RETRIES") or 6

ALLOWED_HOSTS = (
    os.environ.get("ALLOWED_HOSTS").split(",")
    if os.environ.get("ALLOWED_HOSTS")
    else ["127.0.0.1"]
)

CSRF_TRUSTED_ORIGINS = ["http://localhost:81"]

INTERNAL_IPS = (
    os.environ.get("INTERNAL_HOSTS").split(",")
    if os.environ.get("INTERNAL_HOSTS")
    else ["127.0.0.1"]
)

BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": ConnectionError,
    "max_tries": BACKOFF_MAX_RETRIES,
}

CIRCUIT_CONFIG = {"failure_threshold": 5, "expected_exception": ConnectionError}

include(
    "components/*.py",
)
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

STATIC_URL = "static/"
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}
