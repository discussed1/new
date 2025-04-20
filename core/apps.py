from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """
        Method called by Django when the app is ready.
        We import and call our ready function here.
        """
        import core
        core.ready()
