ADMINS = [("Engineering Team", "engineering@jetstreamafrica.com")]
MANAGERS = [("Engineering Team", "engineering@jetstreamafrica.com")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS ORIGIN
CORS_ORIGIN_ALLOW_ALL = False

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

EMAIL_USE_TLS = True

# CELERY BROKER SETTINGS

BROKER_CONNECTION = None
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

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
