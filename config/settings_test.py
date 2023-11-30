import sys

from .settings import *

SECRET_KEY = "test_secret_key"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}


if "create-db" not in sys.argv:
    DATABASES["default"]["TEST"]["NAME"] = f"{BASE_DIR}/test.db.sqlite3"
