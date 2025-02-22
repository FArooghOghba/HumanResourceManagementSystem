from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.hr_management_system.users'
    label = 'users'  # This label is what Django will use to refer to the app
