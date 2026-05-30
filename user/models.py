from __future__ import annotations

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.utils.translation import gettext as _


class UserManager(DjangoUserManager):
    use_in_migrations = True


class User(AbstractUser):
    username = None
    email = models.EmailField(_("Email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()
