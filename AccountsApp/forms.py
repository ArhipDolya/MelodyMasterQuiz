from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from .validators import validate_unique_password, CustomMinimumLengthValidator


class RegisterForm(UserCreationForm):

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        user = getattr(self, 'user', None)
        
        try:
            password_validation.validate_password(password1, user)
        except forms.ValidationError as error:
            self.add_error('password1', error)

        if password1:
            validate_unique_password(password1, user)

        return password1

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=90, widget=forms.PasswordInput)

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            user = authenticate(request=self.request, username=username_or_email, password=password)
            
            if user is None:
                raise forms.ValidationError('Invalid login credentials')

            self.cleaned_data['user'] = user
            
        return username_or_email