import os
from .common import Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = ('whitenoise.runserver_nostatic', ) + Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package=pubtrack'
    ]

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
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'corsheaders.middleware.CorsPostCsrfMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

    )

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_REPLACE_HTTPS_REFERER = True

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'