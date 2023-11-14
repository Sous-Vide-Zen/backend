from datetime import timedelta
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY", default="bad-key-_$i&ghy42$5ki+155q9$dpz6e410wec7adv*c3u0@6tjn7&yv+"
)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = []

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
    "taggit",
    # apps
    "src.apps.users",
    "src.apps.recipes",
    "src.apps.favorite",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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


DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {},
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    #     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    #     "ROTATE_REFRESH_TOKENS": False,
    #     "BLACKLIST_AFTER_ROTATION": False,
    #     "UPDATE_LAST_LOGIN": False,
    #     "ALGORITHM": "HS256",
    #     "SIGNING_KEY": SECRET_KEY,
    #     "VERIFYING_KEY": "",
    #     "AUDIENCE": None,
    #     "ISSUER": None,
    #     "JSON_ENCODER": None,
    #     "JWK_URL": None,
    #     "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    #     "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    #     "USER_ID_FIELD": "id",
    #     "USER_ID_CLAIM": "user_id",
    #     "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    #     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    #     "TOKEN_TYPE_CLAIM": "token_type",
    #     "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    #     "JTI_CLAIM": "jti",
    #     "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    #     "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    #     "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    #     "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    #     "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    #     "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    #     "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    #     "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    #     "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

AUTHENTICATION_BACKENDS = (
    "social_core.backends.vk.VKOAuth2",
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

MEDIA_URL = "src/media/"
MEDIA_ROOT = BASE_DIR / "src/media"

# User model

AUTH_USER_MODEL = "users.CustomUser"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SWAGGER_SETTINGS

# SWAGGER_SETTINGS = {
#     "SECURITY_DEFINITIONS": {
#         "JWT [Bearer {JWT}]": {
#             "name": "Authorization",
#             "type": "apiKey",
#             "in": "header",
#         }
#     },
#     "USE_SESSION_AUTH": False,
# }


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
