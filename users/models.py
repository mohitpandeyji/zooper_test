import time

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from zooper.utilities.model_mixins import Timestampable
from users.managers import UserManager


class User(PermissionsMixin, AbstractBaseUser, Timestampable):
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def _profile_picture_upload_location(self, filename):
        return f"profile-pictures/{self.user.username}/{filename}"

    token = models.CharField(max_length=7, unique=True)
    first_name = models.CharField(
        _('first name'),
        max_length=255, null=True, blank=True)

    last_name = models.CharField(
        _('last name'),
        max_length=255, null=True, blank=True)

    # This field is for better searching.
    full_name = models.CharField(
        _('full name'),
        max_length=255,
        blank=True
    )

    email = models.EmailField(
        _('email address'), unique=True)

    is_staff = models.BooleanField(_("is staff"), default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name} – {self.email}"

    # pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        self.token = self._generate_unique_token()
        self.full_name = self.get_full_name()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name) if self.first_name and self.last_name else ''

    @staticmethod
    def _generate_unique_token():
        """
        Generate a new token, and return it only if it cannot be found in the database. Repeat if necessary.

        :return: Unique token
        """
        token = get_random_string(length=6, allowed_chars="0123456789")
        timeout = time.time() + 5  # 5 seconds from now
        while User.objects.filter(token=token).exists():
            token = get_random_string(length=20, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            if time.time() > timeout:
                raise TimeoutError

        return token
