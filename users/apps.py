from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_save = "django.db.BigAutoField"
    name = 'users'

    def ready(self):
        import users.signal
        