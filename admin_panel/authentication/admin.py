from django.contrib import admin

from authentication.models.auth import (
    ThirdPartyUser,
    UsersHistory,
)
from authentication.models.roles import Role, UserRole
from authentication.models.users import User
from utils.use_db_admin_mixin import UseDbAdminMixin


class AuthModelAdmin(UseDbAdminMixin):
    """Определяем БД для работы."""

    using = 'auth_db'


@admin.register(UsersHistory,)
class UsersHistoryAdmin(AuthModelAdmin):
    """История входов пользователя."""

    list_display = 'user', 'source', 'login_time'
    search_fields = 'user', 'source'
    raw_id_fields = 'user',
    list_select_related = True


@admin.register(Role,)
class RoleAdmin(AuthModelAdmin):
    """Роли пользователя."""

    list_display = 'title', 'permissions'
    search_fields = 'title', 'permissions'


@admin.register(UserRole,)
class UserRoleAdmin(AuthModelAdmin):
    """Связь пользователя и его роли."""

    list_display = 'user', 'role'
    search_fields = 'user', 'role'
    list_select_related = True
    raw_id_fields = 'user', 'role'


@admin.register(User,)
class UserAdmin(AuthModelAdmin):
    """Пользователи."""

    list_display = 'email', 'first_name', 'last_name', 'disabled'
    search_fields = 'email', 'first_name', 'last_name'


@admin.register(ThirdPartyUser,)
class ThirdPartyUserAdmin(AuthModelAdmin):
    """Пользователь стороннего сервиса."""

    list_display = 'user', 'third_party_id', 'third_party_title'
    search_fields = 'user', 'third_party_id', 'third_party_title'
    raw_id_fields = 'user',
    list_select_related = True
