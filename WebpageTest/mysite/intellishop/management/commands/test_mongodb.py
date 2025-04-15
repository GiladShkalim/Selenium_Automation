from django.core.management.base import BaseCommand
from intellishop.utils.mongodb_utils import get_db_handle

class Command(BaseCommand):
    help = 'Test MongoDB connection'

    def handle(self, *args, **options):
        try:
            db, client = get_db_handle()
            server_info = client.server_info()
            self.stdout.write(self.style.SUCCESS(f'Successfully connected to MongoDB version: {server_info["version"]}'))
            self.stdout.write(self.style.SUCCESS(f'Available databases: {client.list_database_names()}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to MongoDB: {e}'))
        finally:
            if 'client' in locals():
                client.close()
