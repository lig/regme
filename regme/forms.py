from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class UserCreationForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.

    Based on `django.contrib.auth.forms.UserCreationForm`.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    email = forms.EmailField(label=_("Email"), max_length=254,
        help_text=_("Required valid email. 254 characters or fewer."),
        error_messages={
            'invalid': _("This value may contain only valid email address.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self):
        user = User._default_manager.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data["password1"])
        return user


class UserActivationForm(forms.Form):

    user = None
    error_messages = {
        'wrong_activation_key': _("Wrong activation key."),
        'user_already_activated': _("User already activated."),
    }
    username = forms.CharField(label=_("Username"), max_length=30)
    activation_key = forms.CharField(label=_("Activation key"))

    def clean(self):

        if self.cleaned_data.keys() == {'username', 'activation_key'}:

            try:
                user = User._default_manager.get(
                    username=self.cleaned_data['username'])
            except User.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['wrong_activation_key'],
                    code='wrong_activation_key')

            if user.activate(self.cleaned_data['activation_key'], save=False):
                self.user = user
            elif user.is_active:
                raise forms.ValidationError(
                    self.error_messages['user_already_activated'],
                    code='user_already_activated')
            else:
                raise forms.ValidationError(
                    self.error_messages['wrong_activation_key'],
                    code='wrong_activation_key')

    def save(self):

        if self.user:
            self.user.save()
            return self.user
