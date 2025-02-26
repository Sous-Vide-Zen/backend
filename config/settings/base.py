from datetime import timedelta
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config(
    "SECRET_KEY", default="bad-key-_$i&ghy42$5ki+155q9$dpz6e410wec7adv*c3u0@6tjn7&yv+"
)

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Сторонние библиотеки
    "rest_framework",
    "djoser",
    "rest_framework_simplejwt",
    "drf_yasg",
    "social_django",
    "django_filters",
    "taggit",
    "corsheaders",
    "phonenumber_field",
    # Приложения проекта
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

WSGI_APPLICATION = "config.wsgi.application"

# Настройки Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_THROTTLE_RATES": {"reactions": "100/second"},
}

# Настройки Djoser
DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "api/v1/auth/users/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "api/v1/auth/activate/{uid}/{token}",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
    "PERMISSIONS": {
        "user_delete": ["rest_framework.permissions.IsAdminUser"],
    },
    "SERIALIZERS": {
        "user_create_password_retype": "src.apps.users.serializers.CustomUserCreateSerializer",
        "current_user": "src.apps.users.serializers.CustomUserMeSerializer",
        "user": "src.apps.users.serializers.CustomUserSerializer",
    },
    "EMAIL": {
        "activation": "src.apps.users.emails.CustomActivationEmail",
        "password_reset": "src.apps.users.emails.CustomPasswordResetEmail",
    },
}

# Настройки Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Аутентификация
AUTHENTICATION_BACKENDS = (
    "config.plugin_soc_auth.CustomVKOAuth2",
    "social_core.backends.yandex.YandexOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "src.base.validators.CustomPasswordValidator"},
    {"NAME": "src.base.validators.NoUpperCaseValidator"},
    {"NAME": "src.base.validators.NoLowerCaseValidator"},
    {"NAME": "src.base.validators.NoNumbersValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
]

# Интернационализация
LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Статические файлы и медиа
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "src/static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "src/media"

# Пользовательская модель и тип первичного ключа
AUTH_USER_MODEL = "users.CustomUser"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки Swagger
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

# Настройки социальных сетей (ключи из .env)
SOCIAL_AUTH_VK_OAUTH2_KEY = config("SOCIAL_AUTH_VK_OAUTH2_KEY", default="12345678")
SOCIAL_AUTH_VK_OAUTH2_SECRET = config(
    "SOCIAL_AUTH_VK_OAUTH2_SECRET", default="12345678"
)
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = config(
    "SOCIAL_AUTH_YANDEX_OAUTH2_KEY", default="12345678"
)
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = config(
    "SOCIAL_AUTH_YANDEX_OAUTH2_SECRET", default="12345678"
)
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = config(
    "SOCIAL_AUTH_LOGIN_REDIRECT_URL", default="/api/v1/auth/o/vk_oauth2/"
)

# Настройки django-taggit
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True

# Настройки CORS
CORS_ALLOW_ALL_ORIGINS = True

# Пагинация
COMMENT_PAGE_SIZE = 10
FEED_PAGE_SIZE = 5
FOLLOWER_PAGE_SIZE = 10
USER_LIST_PAGE_SIZE = 10

# Переменные проекта
ACTIVITY_INTERVAL = 30
DRAFTS_MAX_AMOUNT = 3
SHORT_RECIPE_SYMBOLS = 100
SHORT_BIO_SYMBOLS = 50
TIME_FROM_VIEW_RECIPE = 20
REGEX = r"^[a-zA-Zа-яА-Я\s\-\‘\u00C0-\u017F]+$"
