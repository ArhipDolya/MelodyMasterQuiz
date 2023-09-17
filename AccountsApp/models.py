from django.db import models
from django.contrib.auth.models import User


class UsedPassword(models.Model):
    """
    Model representing used passwords for a user
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    

    def __str__(self):
        return f'Used password for {self.user.username}'