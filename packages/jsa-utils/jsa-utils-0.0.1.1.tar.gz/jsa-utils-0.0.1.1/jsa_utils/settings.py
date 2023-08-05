import os
from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_BASE_URL = os.environ.get("SERVICE_BASE_URL", config("SERVICE_BASE_URL", "-"))
AUTH_BASE_URL = os.environ.get("AUTH_BASE_URL", config("AUTH_BASE_URL", "-"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", config("SECRET_KEY", "-"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", config("DEBUG", True)))

ALLOWED_HOSTS = str(
    os.environ.get("ALLOWED_HOSTS", config("ALLOWED_HOSTS", "localhost,127.0.0.1"))
).split(",")

ADMINS = [("Engineering Team", "engineering@jetstreamafrica.com")]
MANAGERS = [("Engineering Team", "engineering@jetstreamafrica.com")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

# CORS ORIGIN
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = tuple(
    link.strip()
    for link in os.environ.get(
        "CORS_WHITELIST", config("CORS_WHITELIST", "http://localhost:8080")
    ).split(",")
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Email Settings
EMAIL_HOST = os.environ.get("EMAIL_HOST", config("EMAIL_HOST", "-"))
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", config("EMAIL_PORT", "000")))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", config("EMAIL_HOST_USER", "-"))
EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD", config("EMAIL_HOST_PASSWORD", "-")
)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", config("DEFAULT_FROM_EMAIL", "-")
)

# CELERY BROKER SETTINGS

MESSAGING_USERNAME = os.environ.get(
    "MESSAGING_USERNAME", config("MESSAGING_USERNAME", "-")
)
MESSAGING_PWORD = os.environ.get("MESSAGING_PWORD", config("MESSAGING_PWORD", "-"))
BROKER_IP = os.environ.get("BROKER_IP", config("BROKER_IP", "-"))
BROKER_PORT = os.environ.get("BROKER_PORT", config("BROKER_PORT", "-"))
BROKER_VHOST = os.environ.get("BROKER_VHOST", config("BROKER_VHOST", "-"))
BROKER_CONNECTION = None
CELERY_BROKER_URL = "amqp://{}:{}@{}:{}/{}".format(
    MESSAGING_USERNAME, MESSAGING_PWORD, BROKER_IP, BROKER_PORT, BROKER_VHOST
)
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
APPLICATION_ID = os.environ.get("APPLICATION_ID", config("APPLICATION_ID", "-"))
CELERY_TASK_QUEUES = (
    Queue(
        str(APPLICATION_ID).upper() + "_INBOX",
        Exchange("JETSTREAM_DX"),
        routing_key=APPLICATION_ID + "_inbox",
    ),
)
ROUTING_EXCHANGES = [
    {
        "id": "jetstream_BX",
        "type": "fanout",
        "description": "Jetstream Platform Broadcast Exchange",
    },
    {
        "id": "jetstream_DX",
        "type": "direct",
        "description": "Jetstream Platform Direct Exchange",
    },
    {
        "id": "jetstream_TX",
        "type": "topic",
        "description": "Jetstream Platform Topic Exchange",
    },
]
