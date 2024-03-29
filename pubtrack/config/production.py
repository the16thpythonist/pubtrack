import os
from .common import Common

BASE_DIR = '/code'


class Production(Common):
    DEBUG = False

    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    INSTALLED_APPS += ("gunicorn", )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        # development only
        'django.middleware.security.SecurityMiddleware',
        # WhiteNoise is a project which delivers static files directly from the python web server, which eliminates the
        # need for the separate nginx reverse proxy: http://whitenoise.evans.io/en/stable/.
        # This is the better alternative since this project is not meant to serve big traffic anyways and neither is it
        # supposed to be publicly available.
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 100)),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    # This line enables all the optimizations which WhiteNoise provides in contrast to the default Django static file
    # serving. That includes the appropriate generation of caching headers and the auto compression of large files.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    #Common.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer', )

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    # http://django-storages.readthedocs.org/en/latest/index.html

    # INSTALLED_APPS += ('storages',)
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY')
    # AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME')
    # AWS_DEFAULT_ACL = 'public-read'
    # AWS_AUTO_CREATE_BUCKET = True
    # AWS_QUERYSTRING_AUTH = False
    # MEDIA_URL = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'
    #
    # # https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#cache-control
    # # Response can be cached by browser and any intermediary caches (i.e. it is "public") for up to 1 day
    # # 86400 = (60 seconds x 60 minutes x 24 hours)
    # AWS_HEADERS = {
    #     'Cache-Control': 'max-age=86400, s-maxage=86400, must-revalidate',
    # }
