from pathlib import Path
import os 
from datetime import timedelta
import ssl
from django.core.mail.backends.smtp import EmailBackend
import environ
import dj_database_url

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'TRUE' 

AUTH_USER_MODEL = 'api.MyUser'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '3000', os.environ.get('RENDER_HOSTNAME', '')]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
    'api',
    'crispy_forms', #Updated here
    'crispy_bootstrap5', #Updated here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=120),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=140),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# Create a custom SSL context with custom options
custom_ssl_context = ssl.create_default_context()
custom_ssl_context.check_hostname = False  # Disable hostname verification
custom_ssl_context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

# Pass the custom SSL context to the EmailBackend
email_backend = EmailBackend(ssl_context=custom_ssl_context)

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

SIMPLE_JWT = {
  "TOKEN_OBTAIN_SERIALIZER": "api.serializers.MyTokenObtainPairSerializer",
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# dj_database_url will load the database from the environment variable DATABASE_URL, if it exists,
# otherwise falling back to the default sqlite database.


DATABASES = {
    'default': dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    }

DATABASE_NAME = env('DATABASE_NAME')
DATABASE_USER = env('DATABASE_USER')
DATABASE_PASSWORD = env('DATABASE_PASSWORD')
DATABASE_HOST = env('DATABASE_HOST')
DATABASE_PORT = env('DATABASE_PORT')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'frontend/src/static/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"


