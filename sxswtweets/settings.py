"""
Django settings for sxswtweets project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('DEBUG', 'False') == 'True')

TEMPLATE_DEBUG = (os.environ.get('DEBUG', 'False') == 'True')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'tastypie',
    'haystack',
    'storages',
    'sxsw'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sxswtweets.urls'

WSGI_APPLICATION = 'sxswtweets.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

S3_ENABLED = (os.environ.get('S3_ENABLED', 'False') == 'True')
DEFAULT_FILE_STORAGE = 'sxswtweets.s3utils.MediaS3BotoStorage'
if S3_ENABLED:
    STATICFILES_STORAGE = 'sxswtweets.s3utils.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ['S3_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['S3_SECRET']
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET']
AWS_QUERYSTRING_AUTH = (os.environ.get('S3_QUERYSTRING_AUTH', 'False') == 'True')

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
CLOUDFRONT_DOMAIN = 'static.upwordsxsw.com'

STATIC_DIRECTORY = '/static/'
MEDIA_DIRECTORY = '/media/'

MEDIA_ROOT = ''
MEDIA_URL = S3_URL + MEDIA_DIRECTORY
if S3_ENABLED:
    STATIC_ROOT = ''
    STATIC_URL = S3_URL + STATIC_DIRECTORY
else :
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ.get('BONSAI_URL', 'http://127.0.0.1:9200/'),
        'INDEX_NAME': 'haystack',
    },
}

# Remap Memcachier environment variables to something django-pylibmc understands
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '127.0.0.1').replace(',', ';')
if os.environ.get('MEMCACHIER_USERNAME'):
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME')
if os.environ.get('MEMCACHIER_PASSWORD'):
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD')

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': {  # Maps to pylibmc "behaviors"
            'tcp_nodelay': True,
            'ketama': True
        }
    }
}

print os.environ['DATABASE_URL']