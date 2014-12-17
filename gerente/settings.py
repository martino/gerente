"""
Django settings for gerente project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '89z+y@6mi3@b&d801nd4!5705e^gvv_7o)25!uuy_7fe@&-4pw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'clasificador',
    'pruebas',
    'documentos',
    'rest_framework',
    'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gerente.urls'

WSGI_APPLICATION = 'gerente.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

APP_ID = '***REMOVED***'
APP_KEY = '163560ca***REMOVED***'
DATATXT = 'https://api.dandelion.eu'


CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = 'redis://localhost:6379/5'

MODEL_MAPPINGS = [{
    u'neo liberism': 'NL',
    u'labour vs capital': 'LVSC',
    u'developmental state': 'DS',
    u'continental capitalism': 'CC',
    u'stigma lottizzazione': 'SI SL CSVP',
    u'capture view privatization': 'CVP',
    u'protecting rents': 'PR',
    u'technical pragmatical view': 'TPV EF',
    u'captious view privatizaion': 'SI SL CSVP',
    u'european forces': 'TPV EF',
    u'stigma inertia boiardi': 'SI SL CSVP',
    u'taken for grantedness': 'TFG',
}]
