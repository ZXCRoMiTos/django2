from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import HiddenInput, forms
import hashlib
import random


class ShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'


class AgeValidatorMixin:
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        return age


class ShopUserCreationForm(AgeValidatorMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "password1", "password2", "email", "age")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

    def save(self):
        user = super(ShopUserCreationForm, self).save()
        user.is_activate = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserChangeForm(AgeValidatorMixin, UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password", "email", "first_name", "last_name",
                  "age", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = HiddenInput()
                continue
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''
