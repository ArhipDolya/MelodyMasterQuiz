from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    pass



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