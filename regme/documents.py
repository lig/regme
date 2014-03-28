from datetime import datetime, timedelta
from hashlib import sha1
from random import random

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from mongoengine import StringField, DateTimeField
from mongoengine.django.auth import User as BaseUser
from mongoengine.signals import pre_save


class User(BaseUser):

    activation_key = StringField()
    activation_due = DateTimeField()

    @staticmethod
    def ensure_inactive(klass, document):

        if document.id is None and not document.is_superuser:
            document.deactivate(save=False)

    @staticmethod
    def make_key():
        return sha1((settings.SECRET_KEY + str(random())).encode()).hexdigest()

    def deactivate(self, save=True, notify=True):
        self.is_active = False
        self.activation_key = self.make_key()
        self.activation_due = (
            datetime.utcnow() + timedelta(
                days=settings.ACCOUNT_ACTIVATION_DAYS))

        if save:
            self.save()

        if notify:
            c = {
                'site': settings.SITE,
                'user': self,
            }
            subject = render_to_string(
                'registration/email/activate_subject.txt', c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = render_to_string(
                'registration/email/activate_email.txt', c)
            send_mail(subject, email, None, [self.email])

        return True

    def activate(self, activation_key, save=True):

        if self.activation_key != activation_key:
            return False
        if self.activation_due < datetime.utcnow():
            return False
        if self.is_active:
            return False

        self.is_active = True
        if save:
            self.save()
        return True

    def has_usable_password(self):
        """Dummy method for django.contrib.auth.forms.PasswordResetForm
        compatibility
        """
        return True

pre_save.connect(User.ensure_inactive, User)
