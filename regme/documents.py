from hashlib import sha1
from random import random

from django.conf import settings
from mongoengine.django.auth import User as BaseUser
from mongoengine.signals import pre_save
from mongoengine import StringField


class User(BaseUser):

    activation_key = StringField()

    @staticmethod
    def ensure_inactive(klass, document):

        if document.id is None and not document.is_superuser:
            document.deactivate(save=False)

    @staticmethod
    def make_key():
        return sha1((settings.SECRET_KEY + str(random())).encode()).hexdigest()

    def deactivate(self, save=True):
        self.is_active = False
        self.activation_key = self.make_key()
        if save:
            self.save()

    def activate(self, activation_key, save=True):
        if self.activation_key == activation_key:
            self.is_active = True
            if save:
                self.save()

pre_save.connect(User.ensure_inactive, User)
