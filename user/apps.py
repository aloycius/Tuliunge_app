from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

class RidesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rides'

class Tuliunge_backendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tuliunge_backend'
