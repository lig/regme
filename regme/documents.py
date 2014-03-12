from hashlib import sha1
from random import random

from django.conf import settings
from mongoengine.django.auth import User as BaseUser
from mongoengine.signals import pre_save


class User(BaseUser):

    def get_activation_key(self):
        return sha1((settings.SECRET_KEY + str(random())).encode()).hexdigest()

    @staticmethod
    def ensure_inactive(klass, document):

        if document.id is None:
            document.is_active = False


pre_save.connect(User.ensure_inactive, User)
