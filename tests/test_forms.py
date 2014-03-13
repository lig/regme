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
