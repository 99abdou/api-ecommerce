from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'  # email utilisé pour se connecter
    REQUIRED_FIELDS = ['username']  # username requis à la création

    def __str__(self):
        return self.email
