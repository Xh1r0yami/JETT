from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # <- tambahkan ini
    name = 'accounts'

    def ready(self):
        import accounts.signals
