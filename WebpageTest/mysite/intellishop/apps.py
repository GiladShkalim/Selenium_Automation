# Application configuration settings for the IntelliShop app

from django.apps import AppConfig

class IntellishopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'intellishop'
    
    def ready(self):
        # Import and run initialization
        from .utils.initialize_db import initialize_database
        try:
            initialize_database()
        except Exception as e:
            # Log the error but don't prevent app from starting
            print(f"MongoDB initialization error: {e}")
