from enum import Enum


class DefaultDb(Enum):
    auth = 'auth'
    contenttypes = 'contenttypes'
    sessions = 'sessions'
    admin = 'admin'
    administrator = 'administrator'


class DataBase(Enum):
    default = 'default'
    authentication = 'auth_db'
    movie = 'movie_db'
    notification = 'notification_db'
    user_profile = 'profile_db'


class CustomRouter:
    """A router to control all database operations on models in the auth
    and contenttypes applications."""

    route_app_labels = {'auth', 'contenttypes', 'sessions', 'admin'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        match model._meta.app_label:
            case (DefaultDb.auth.value |
                  DefaultDb.contenttypes.value |
                  DefaultDb.sessions.value |
                  DefaultDb.administrator.value |
                  DefaultDb.admin.value):
                return DataBase.default.value
            case DataBase.authentication.name:
                return DataBase.authentication.value
            case DataBase.movie.name:
                return DataBase.movie.value
            case DataBase.notification.name:
                return DataBase.notification.value
            case DataBase.user_profile.name:
                return DataBase.user_profile.value
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        match model._meta.app_label:
            case (DefaultDb.auth.value |
                  DefaultDb.contenttypes.value |
                  DefaultDb.sessions.value |
                  DefaultDb.administrator.value |
                  DefaultDb.admin.value):
                return DataBase.default.value
            case DataBase.authentication.name:
                return DataBase.authentication.value
            case DataBase.movie.name:
                return DataBase.movie.value
            case DataBase.notification.name:
                return DataBase.notification.value
            case DataBase.user_profile.name:
                return DataBase.user_profile.value
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if any((
            (obj1._meta.app_label in self.route_app_labels
             or obj2._meta.app_label in self.route_app_labels),
            obj1._meta.app_label == obj2._meta.app_label,
        )):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        match app_label:
            case (DefaultDb.auth.value |
                  DefaultDb.contenttypes.value |
                  DefaultDb.sessions.value |
                  DefaultDb.administrator.value |
                  DefaultDb.admin.value):
                return DataBase.default.value
            case DataBase.authentication.name:
                return DataBase.authentication.value
            case DataBase.movie.name:
                return DataBase.movie.value
            case DataBase.notification.name:
                return DataBase.notification.value
            case DataBase.user_profile.name:
                return DataBase.user_profile.value
        return None
