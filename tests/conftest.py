from os import path
import sys

from django.conf import settings
import django
import pytest


sys.path[0:0] = ['']


@pytest.fixture(scope='session')
def django_settings():
    settings.configure(
        USE_TZ=True,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'mongoengine.django.mongo_auth',
            'regme',
        ),
        AUTH_USER_MODEL='mongo_auth.MongoUser',
        AUTHENTICATION_BACKENDS=(
            'mongoengine.django.auth.MongoEngineBackend',),
        MONGOENGINE_USER_DOCUMENT='regme.documents.User',
        ACCOUNT_ACTIVATION_DAYS=7,
        DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}},
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        TEMPLATE_DIRS=(
            path.join(
                path.dirname(django.__file__),
                'contrib', 'auth', 'tests', 'templates'),
        ),
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
        ),
    )
