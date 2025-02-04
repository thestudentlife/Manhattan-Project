"""
Django settings for website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALLOWED_HOSTS = ['.tsl.news','.tsl.pomona.edu','127.0.0.1','localhost']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_mobile',
    'pysolr',
    'haystack',
    'geoposition',
    'widget_tweaks',
    'autocomplete_light',
    'mainsite',
    'workflow'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
)

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django_mobile.context_processors.flavour',
    'mainsite.context_processors.section'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django_mobile.loader.Loader',
)

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

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
ENV_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

PROJECT_PATH = os.path.join(ENV_PATH, os.pardir)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'mainsite', 'static'),
    os.path.join(PROJECT_PATH, 'workflow', 'static')
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = '/workflow/login'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://tsl.pomona.edu:8983/solr'
    },
}

# Only for development
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.mail.yahoo.com"
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'claremont_academia@yahoo.com'

GEOPOSITION_MAP_WIDGET_HEIGHT = 240

FILE_UPLOAD_PERMISSIONS = 0o644



