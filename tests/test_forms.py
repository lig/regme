from random import seed

from mongoengine import connect
import pytest


@pytest.fixture
def User(django_settings):
    from regme.documents import User
    return User


@pytest.yield_fixture
def db(User):
    connect(db='test_regme')
    User.drop_collection()
    yield
    User.drop_collection()


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


def test_user_creation_form(user_data, db):
    from regme.forms import UserCreationForm
    form = UserCreationForm({
        'username': user_data['username'],
        'email': user_data['email'],
        'password1': user_data['password'],
        'password2': user_data['password'],
    })
    assert bool(form.is_valid())
    user = form.save()
    assert not user.is_active


def test_user_activation_form(user_data, user):
    from regme.forms import UserActivationForm
    form = UserActivationForm({
        'username': user.username,
        'activation_key': user.activation_key,
    })
    assert bool(form.is_valid())
    user = form.save()
    assert user.is_active


def test_user_activation_form_unknown_username(user_data, user):
    from regme.forms import UserActivationForm
    form = UserActivationForm({
        'username': user.username + 'test',
        'activation_key': user.activation_key,
    })
    assert not bool(form.is_valid())
    assert form.user is None
    assert form.save() is None


def test_user_activation_form_empty_username(user_data, user):
    from regme.forms import UserActivationForm
    form = UserActivationForm({
        'username': '',
        'activation_key': user.activation_key,
    })
    assert not bool(form.is_valid())
    assert form.user is None
    assert form.save() is None


def test_user_activation_form_wrong_activation_key(user_data, user):
    from regme.forms import UserActivationForm
    form = UserActivationForm({
        'username': user.username,
        'activation_key': user.activation_key + 'test',
    })
    assert not bool(form.is_valid())
    assert form.user is None
    assert form.save() is None


def test_user_activation_form_empty_activation_key(user_data, user):
    from regme.forms import UserActivationForm
    form = UserActivationForm({
        'username': user.username,
        'activation_key': '',
    })
    assert not bool(form.is_valid())
    assert form.user is None
    assert form.save() is None


def test_user_activation_form_already_activated(user_data, user):
    from regme.forms import UserActivationForm
    user.activate(user.activation_key)
    form = UserActivationForm({
        'username': user.username,
        'activation_key': user.activation_key,
    })
    assert not bool(form.is_valid())
    assert form.user is None
    assert form.save() is None
