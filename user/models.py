from __future__ import annotations

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.utils.translation import gettext as _


class UserManager(DjangoUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> User:
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields
    ) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractUser):
    username = None
    email = models.EmailField(_("Email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()
