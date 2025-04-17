from django.core.management.base import BaseCommand, CommandError
from intellishop.models.mongodb_models import Coupon
from django.conf import settings
import os
import json
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import coupons from JSON or CSV files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, nargs='?', help='Path to the JSON or CSV file containing coupon data')
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing coupons before importing',
        )
        parser.add_argument(
            '--sample',
            choices=['json', 'csv', 'all'],
            help='Import sample data files from intellishop/data/coupons/',
        )

    def handle(self, *args, **options):
        clear = options.get('clear', False)
        file_path = options.get('file_path')
        sample = options.get('sample')
        
        # Handle sample data import
        if sample:
            base_dir = settings.BASE_DIR
            
            # Clear existing coupons if requested
            if clear:
                self._clear_coupons()
            
            if sample == 'json' or sample == 'all':
                json_path = os.path.join(base_dir, 'intellishop', 'data', 'coupons', 'coupon_samples.json')
                if os.path.exists(json_path):
                    self.stdout.write(f"Importing JSON sample from: {json_path}")
                    self._import_from_file(json_path)
                else:
                    self.stdout.write(self.style.WARNING(f"JSON sample file not found at: {json_path}"))
                
            if sample == 'csv' or sample == 'all':
                csv_path = os.path.join(base_dir, 'intellishop', 'data', 'coupons', 'sample_offers.csv')
                if os.path.exists(csv_path):
                    self.stdout.write(f"Importing CSV sample from: {csv_path}")
                    self._import_from_file(csv_path)
                else:
                    self.stdout.write(self.style.WARNING(f"CSV sample file not found at: {csv_path}"))
                
            return
        
        # Regular file import
        if not file_path:
            self.stdout.write(self.style.ERROR("Error: file_path is required"))
            self.stdout.write("Use --sample json|csv|all to import sample data")
            return
            
        # Check if file exists
        if not os.path.exists(file_path):
            raise CommandError(f'File does not exist: {file_path}')
        
        # Clear existing coupons if requested
        if clear:
            self._clear_coupons()
        
        # Import coupons from file
        self._import_from_file(file_path)
    
    def _clear_coupons(self):
        """Clear all existing coupons from the collection"""
        collection = Coupon.get_collection()
        if collection is not None:
            try:
                result = collection.delete_many({})
                self.stdout.write(self.style.SUCCESS(f'Deleted {result.deleted_count} existing coupons'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error clearing coupons: {str(e)}'))
        else:
            self.stdout.write(self.style.ERROR('Could not access coupons collection'))
    
    def _import_from_file(self, file_path):
        """Import coupons from a file (JSON or CSV)"""
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
            self.stdout.write(f'  Updated: {results.get("updated", 0)}')
            self.stdout.write(f'  New: {results.get("new", 0)}')
            
            if results["errors"]:
                self.stdout.write(self.style.WARNING('\nErrors:'))
                for error in results["errors"][:10]:  # Show only first 10 errors
                    self.stdout.write(f'  - {error}')
                
                if len(results["errors"]) > 10:
                    self.stdout.write(f'  ... and {len(results["errors"]) - 10} more errors') 