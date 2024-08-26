from django.apps import AppConfig


class VpnServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.vpn_service'

    def ready(self):
        from .signals import create_user_profile, save_user_profile
