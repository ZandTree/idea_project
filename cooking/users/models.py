from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    """ signup: username and email; login: email """

    username = models.CharField(_("Username"), unique=True, max_length=120)
    email = models.EmailField(_('Email address'), unique=True, max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    is_banned = models.BooleanField(default=False)
    blackListEmail = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
