from django.core.management.base import BaseCommand
from intellishop.utils.initialize_db import import_sample_coupon_data
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import all sample data from the app data directories'

    def add_arguments(self, parser):
        parser.add_argument('--skip-coupons', action='store_true', help='Skip importing coupon data')

    def handle(self, *args, **options):
        skip_coupons = options.get('skip_coupons', False)
        
        self.stdout.write(self.style.SUCCESS('Starting sample data import...'))
        
        # Import coupon data
        if not skip_coupons:
            self.stdout.write('Importing coupon data...')
            import_sample_coupon_data()
            self.stdout.write(self.style.SUCCESS('Coupon data import completed'))
        
        # Future: Add more data import functions here
        # import_sample_product_data()
        # import_sample_user_data()
        
        self.stdout.write(self.style.SUCCESS('All sample data imports completed successfully')) 