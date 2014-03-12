from mongoengine.django.auth import User as BaseUser
from mongoengine.signals import pre_save


class User(BaseUser):

    @staticmethod
    def ensure_inactive(klass, document):

        if document.id is None:
            document.is_active = False


pre_save.connect(User.ensure_inactive, User)
