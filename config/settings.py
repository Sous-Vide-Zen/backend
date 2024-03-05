from datetime import timedelta
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY", default="bad-key-_$i&ghy42$5ki+155q9$dpz6e410wec7adv*c3u0@6tjn7&yv+"
)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "djoser",
    "rest_framework_simplejwt",
    "drf_yasg",
    "social_django",
    "django_filters",
    "taggit",
    "corsheaders",
    "phonenumber_field",
    # apps
    "src.apps.users",
    "src.apps.recipes",
    "src.apps.comments",
    "src.apps.favorite",
    "src.apps.reactions",
    "src.apps.ingredients",
    "src.apps.view",
    "src.apps.follow",
    "src.apps.feed",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.yandex.ru")
EMAIL_PORT = config("EMAIL_PORT", default=465, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="user@yandex.ru")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="user@yandex.ru")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="password")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "api/v1/auth/users/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "api/v1/auth/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SERIALIZERS": {},
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
    "PERMISSIONS": {
        "user_delete": ["rest_framework.permissions.IsAdminUser"],
    },
    "SERIALIZERS": {
        "current_user": "src.apps.users.serializers.CustomUserMeSerializer",
        "user": "src.apps.users.serializers.CustomUserSerializer",
    },
    "EMAIL": {
        "activation": "src.apps.users.emails.CustomActivationEmail",
        "password_reset": "src.apps.users.emails.CustomPasswordResetEmail",
    },
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

AUTHENTICATION_BACKENDS = (
    "config.plugin_soc_auth.CustomVKOAuth2",
    "social_core.backends.yandex.YandexOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)


WSGI_APPLICATION = "config.wsgi.application"

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "src/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "src/media"

# User model

AUTH_USER_MODEL = "users.CustomUser"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SWAGGER_SETTINGS

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "JWT [Bearer {JWT}]": {
            "name": "Authorization",
            "type": "apiKey",
            "in": "header",
        }
    },
    "USE_SESSION_AUTH": False,
    "DEFAULT_AUTO_SCHEMA_CLASS": "src.apps.swagger.auto_schema_tags.CustomAutoSchema",
}


# Social AUTH Key's

SOCIAL_AUTH_VK_OAUTH2_KEY = config(
    "SOCIAL_AUTH_VK_OAUTH2_KEY", default="b57308fc10884dc5ab8e5f39d728c99d"
)
SOCIAL_AUTH_VK_OAUTH2_SECRET = config(
    "SOCIAL_AUTH_VK_OAUTH2_SECRET", default="60921ea4d2e94741888d5a9ba4009811"
)

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = config(
    "SOCIAL_AUTH_YANDEX_OAUTH2_KEY", default="5fbd3f9c1f4f4d9d9a1f3c9f1f5f7f9f8"
)
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = config(
    "SOCIAL_AUTH_YANDEX_OAUTH2_SECRET", default="5fbd3f9c1f4f4d9d9a1f3c9f1f5f7f9f8"
)


SOCIAL_AUTH_JSONFIELD_ENABLED = True

# Settings for django-taggit

TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True


# Settings for django-cors-headers
CORS_ALLOW_ALL_ORIGINS = True


# Pagination
FEED_PAGE_SIZE = 5
FOLLOWER_PAGE_SIZE = 10

# Variables

ACTIVITY_INTERVAL = 30

# Shorthand

SHORT_RECIPE_SYMBOLS = 100
SHORT_BIO_SYMBOLS = 50

# TIME

TIME_FROM_VIEW_RECIPE = 20
