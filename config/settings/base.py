import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

APP_NAME = 'Belvo Admission Test'
APP_DESCRIPTION = _('Admission Test for Belvo Company')
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
BASE_DIR = Path(__file__).parent.parent.parent
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages'
]
LOCAL_APPS = [
    'applications.apps.Core'
]
EXTERNAL_APPS = []
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + EXTERNAL_APPS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
SECRET_KEY = os.getenv('SECRET_KEY')
WSGI_APPLICATION = 'config.wsgi.application'

# region Internationalization
LANGUAGE_CODE = 'es'
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGES = [('es', _('Spanish'))]
TIME_ZONE = 'America/Montevideo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# endregion
