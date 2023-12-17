from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models.base import TimeStampedMixin, UUIDMixin
from authentication.models.users import User


class Role(UUIDMixin):

    title = models.CharField(
        _('Title'),
        max_length=128,
        unique=True,
    )
    permissions = models.IntegerField(_('Permissions'))

    class Meta:
        db_table = 'auth"."roles'
        managed = False

    def __str__(self):
        return f'<Role {self.title}>'


class UserRole(UUIDMixin):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name=_('Role'),
    )

    class Meta:
        db_table = 'auth"."users_roles'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                name='unique_user_role',
            ),
        ]
        managed = False
