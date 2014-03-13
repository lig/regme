from datetime import datetime, timedelta
from random import seed

from django.conf import settings
from mongoengine import connect
import pytest


@pytest.fixture(scope='module')
def django_settings():
    settings.configure(
        USE_TZ=True,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'mongoengine.django.mongo_auth',
            'regme',
        ),
        AUTH_USER_MODEL=('mongo_auth.MongoUser'),
        AUTHENTICATION_BACKENDS=(
            'mongoengine.django.auth.MongoEngineBackend',),
        MONGOENGINE_USER_DOCUMENT='regme.documents.User',
        ACCOUNT_ACTIVATION_DAYS=7,
    )


@pytest.fixture
def User(django_settings):
    from regme.documents import User
    return User


@pytest.yield_fixture
def db(User):
    connect(db='test_regme')
    User.drop_collection()
    yield


@pytest.fixture
def user_data():
    return {
        'username': 'username',
        'password': 'password',
        'email': 'email@example.com'}


@pytest.fixture
def user(db, User, user_data):
    seed('')
    return User.create_user(**user_data)


def test_create_inactive_user(user, User):
    assert isinstance(user, User)
    assert not user.is_active
    assert user.activation_key == '516bb9061d58280acd0c3900e18feaf5166f02ff'


def test_user_activate_deactivate(user):
    user.activate('516bb9061d58280acd0c3900e18feaf5166f02ff')
    assert user.is_active
    assert user.activation_key == '516bb9061d58280acd0c3900e18feaf5166f02ff'
    user.deactivate()
    assert not user.is_active


def test_user_activate_fail(user):
    user.activate('')
    assert user.activation_key == '516bb9061d58280acd0c3900e18feaf5166f02ff'
    assert not user.is_active


def test_user_activation_expired(user):
    user.activation_due = datetime.utcnow() - timedelta(days=1)
    user.save()
    user.activate('516bb9061d58280acd0c3900e18feaf5166f02ff')
    assert not user.is_active


def test_user_activation_due(user):
    now = datetime.utcnow()
    activation_due_gt = now + timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    activation_due_lt = activation_due_gt - timedelta(days=1)
    assert activation_due_lt < user.activation_due < activation_due_gt
