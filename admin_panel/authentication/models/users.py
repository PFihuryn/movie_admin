from django.db import models

from authentication.models.base import TimeStampedMixin, UUIDMixin
from django.utils.translation import gettext_lazy as _


class User(UUIDMixin, TimeStampedMixin):

    email = models.EmailField(_('Email'), unique=True)
    password = models.CharField(_('Password'), max_length=128)
    first_name = models.CharField(
        _('First name'),
        max_length=128,
        blank=True,
    )
    last_name = models.CharField(
        _('Last name'),
        max_length=128,
        blank=True,
    )
    disabled = models.BooleanField(_('Disabled'), default=False)

    class Meta:
        db_table = 'auth"."users'
        indexes = models.Index(fields=['email', 'password']),
        managed = False

    def __str__(self):
        return f'<User {self.first_name} {self.last_name} with {self.email}>'
