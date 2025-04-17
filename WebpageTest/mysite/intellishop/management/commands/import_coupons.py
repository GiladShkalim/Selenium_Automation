from django.core.management.base import BaseCommand, CommandError
from intellishop.models.mongodb_models import Coupon
import os
import json
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import coupons from JSON or CSV files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON or CSV file containing coupon data')
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing coupons before importing',
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        clear = options['clear']
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise CommandError(f'File does not exist: {file_path}')
        
        # Clear existing coupons if requested
        if clear:
            collection = Coupon.get_collection()
            if collection is not None:
                try:
                    result = collection.delete_many({})
                    self.stdout.write(self.style.SUCCESS(f'Deleted {result.deleted_count} existing coupons'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error clearing coupons: {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR('Could not access coupons collection'))
        
        # Import coupons based on file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        results = None
        if file_ext == '.json':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                results = Coupon.import_from_json(json_data)
            except Exception as e:
                raise CommandError(f'Error importing coupons from JSON: {str(e)}')
        elif file_ext == '.csv':
            try:
                results = Coupon.import_from_csv(file_path)
            except Exception as e:
                raise CommandError(f'Error importing coupons from CSV: {str(e)}')
        else:
            raise CommandError(f'Unsupported file type: {file_ext}. Please use JSON or CSV files.')
        
        # Display results
        if results:
            self.stdout.write(self.style.SUCCESS(f'Processed {results["total"]} coupons:'))
            self.stdout.write(f'  Valid: {results["valid"]}')
            self.stdout.write(f'  Invalid: {results["invalid"]}')
            
            if results["errors"]:
                self.stdout.write(self.style.WARNING('\nErrors:'))
                for error in results["errors"]:
                    self.stdout.write(f'  - {error}') 