from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.contrib.auth.password_validation import get_password_validators
from .models import UsedPassword


def validate_unique_password(password, user=None):
    num_passwords = 5
    if user and user.id:
        used_passwords = UsedPassword.objects.filter(user=user).values_list('password', flat=True)[:num_passwords]
        if password in used_passwords:
            raise ValidationError('This password is already in use. Please, change to another.')

    
class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_help_text(self):
        return f'Your password must contain at least {self.min_length} characters.'