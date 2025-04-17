from django.core.management.base import BaseCommand, CommandError
from intellishop.models.mongodb_models import Coupon
import os
import json
import csv
import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Manage offers/coupons in the database (import, update, remove, list)'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Import command
        import_parser = subparsers.add_parser('import', help='Import offers from a file')
        import_parser.add_argument('file_path', type=str, help='Path to the JSON or CSV file containing offer data')
        import_parser.add_argument('--update', action='store_true', help='Update existing offers instead of skipping them')
        import_parser.add_argument('--clear', action='store_true', help='Clear existing offers before importing')
        
        # Remove command
        remove_parser = subparsers.add_parser('remove', help='Remove offers')
        remove_parser.add_argument('--code', type=str, help='Remove an offer by its code')
        remove_parser.add_argument('--expired', action='store_true', help='Remove all expired offers')
        remove_parser.add_argument('--all', action='store_true', help='Remove all offers')
        
        # List command
        list_parser = subparsers.add_parser('list', help='List offers')
        list_parser.add_argument('--active', action='store_true', help='Show only active (non-expired) offers')
        list_parser.add_argument('--expired', action='store_true', help='Show only expired offers')
        list_parser.add_argument('--code', type=str, help='Filter offers by code (supports partial matching)')
        list_parser.add_argument('--min-amount', type=float, help='Filter offers by minimum amount')
        list_parser.add_argument('--max-amount', type=float, help='Filter offers by maximum amount')
        list_parser.add_argument('--type', type=str, choices=['percent', 'fixed_cart', 'fixed_product'], 
                                help='Filter offers by discount type')
        list_parser.add_argument('--format', type=str, choices=['table', 'json'], default='table',
                                help='Output format (table or json)')

    def handle(self, *args, **options):
        command = options.get('command')
        
        if not command:
            self.print_help('manage.py', 'manage_offers')
            return
            
        # Execute the appropriate command
        if command == 'import':
            self.import_offers(options)
        elif command == 'remove':
            self.remove_offers(options)
        elif command == 'list':
            self.list_offers(options)
        else:
            self.stdout.write(self.style.ERROR(f'Unknown command: {command}'))

    def import_offers(self, options):
        file_path = options['file_path']
        update_existing = options['update']
        clear = options['clear']
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise CommandError(f'File does not exist: {file_path}')
        
        # Clear existing offers if requested
        if clear:
            collection = Coupon.get_collection()
            if collection is not None:
                try:
                    result = collection.delete_many({})
                    self.stdout.write(self.style.SUCCESS(f'Deleted {result.deleted_count} existing offers'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error clearing offers: {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR('Could not access offers collection'))
        
        # Import offers based on file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        offers_to_import = []
        
        if file_ext == '.json':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Handle both single offer and list of offers
                if isinstance(data, list):
                    offers_to_import = data
                else:
                    offers_to_import = [data]
                    
            except json.JSONDecodeError as e:
                raise CommandError(f'Invalid JSON format: {str(e)}')
            except Exception as e:
                raise CommandError(f'Error reading JSON file: {str(e)}')
                
        elif file_ext == '.csv':
            try:
                with open(file_path, 'r', encoding='utf-8') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        # Convert types for CSV data
                        offer = self._convert_csv_types(row)
                        offers_to_import.append(offer)
            except Exception as e:
                raise CommandError(f'Error reading CSV file: {str(e)}')
        else:
            raise CommandError(f'Unsupported file type: {file_ext}. Please use JSON or CSV files.')
        
        # Import offers with validation
        total_count = len(offers_to_import)
        valid_count = 0
        invalid_count = 0
        updated_count = 0
        skipped_count = 0
        errors = []
        
        for offer in offers_to_import:
            # Validate offer
            is_valid, error = Coupon.validate_coupon(offer)
            
            if not is_valid:
                invalid_count += 1
                errors.append(f"Invalid offer {offer.get('code', 'unknown')}: {error}")
                continue
            
            # Check if offer already exists
            existing_offer = Coupon.get_by_code(offer['code'])
            
            if existing_offer:
                if update_existing:
                    # Update existing offer
                    Coupon.update_one({'code': offer['code']}, offer)
                    updated_count += 1
                    valid_count += 1
                else:
                    # Skip existing offer
                    skipped_count += 1
            else:
                # Insert new offer
                Coupon.insert_one(offer)
                valid_count += 1
        
        # Display results
        self.stdout.write(self.style.SUCCESS(f'Processed {total_count} offers:'))
        self.stdout.write(f'  Valid: {valid_count}')
        self.stdout.write(f'  Invalid: {invalid_count}')
        self.stdout.write(f'  Updated: {updated_count}')
        self.stdout.write(f'  Skipped: {skipped_count}')
        
        if errors:
            self.stdout.write(self.style.WARNING('\nErrors:'))
            for error in errors[:10]:  # Show only first 10 errors to avoid flooding
                self.stdout.write(f'  - {error}')
            
            if len(errors) > 10:
                self.stdout.write(f'  ... and {len(errors) - 10} more errors')

    def remove_offers(self, options):
        code = options.get('code')
        remove_expired = options.get('expired')
        remove_all = options.get('all')
        
        collection = Coupon.get_collection()
        if collection is None:
            self.stdout.write(self.style.ERROR('Could not access offers collection'))
            return
            
        if code:
            # Remove specific offer by code
            result = collection.delete_one({'code': code})
            if result.deleted_count > 0:
                self.stdout.write(self.style.SUCCESS(f'Removed offer with code: {code}'))
            else:
                self.stdout.write(self.style.WARNING(f'No offer found with code: {code}'))
                
        elif remove_expired:
            # Remove all expired offers
            current_date = datetime.datetime.utcnow().isoformat()
            result = collection.delete_many({
                'date_expires': {'$lt': current_date}
            })
            self.stdout.write(self.style.SUCCESS(f'Removed {result.deleted_count} expired offers'))
            
        elif remove_all:
            # Remove all offers
            result = collection.delete_many({})
            self.stdout.write(self.style.SUCCESS(f'Removed all offers ({result.deleted_count} total)'))
            
        else:
            self.stdout.write(self.style.WARNING('No removal criteria specified. Use --code, --expired, or --all'))

    def list_offers(self, options):
        active_only = options.get('active')
        expired_only = options.get('expired')
        code_filter = options.get('code')
        min_amount = options.get('min_amount')
        max_amount = options.get('max_amount')
        discount_type = options.get('type')
        output_format = options.get('format', 'table')
        
        # Build query
        query = {}
        
        if active_only:
            current_date = datetime.datetime.utcnow().isoformat()
            query['$or'] = [
                {'date_expires': {'$gt': current_date}},
                {'date_expires': None}
            ]
            
        if expired_only:
            current_date = datetime.datetime.utcnow().isoformat()
            query['date_expires'] = {'$lt': current_date}
            
        if code_filter:
            # Use regex for partial matching
            query['code'] = {'$regex': f'.*{code_filter}.*', '$options': 'i'}
            
        if min_amount is not None:
            query['amount'] = query.get('amount', {})
            query['amount']['$gte'] = min_amount
            
        if max_amount is not None:
            query['amount'] = query.get('amount', {})
            query['amount']['$lte'] = max_amount
            
        if discount_type:
            query['discount_type'] = discount_type
            
        # Get offers
        offers = Coupon.find(query)
        
        if not offers:
            self.stdout.write(self.style.WARNING('No offers found matching the criteria'))
            return
            
        # Display offers
        if output_format == 'json':
            # Convert ObjectIds to strings for JSON serialization
            for offer in offers:
                if '_id' in offer:
                    offer['_id'] = str(offer['_id'])
            self.stdout.write(json.dumps(offers, indent=2))
        else:
            # Table format
            self.stdout.write(f"Found {len(offers)} offers:")
            self.stdout.write("-" * 100)
            self.stdout.write(f"{'CODE':<15} | {'AMOUNT':<8} | {'TYPE':<12} | {'EXPIRES':<20} | {'DESCRIPTION':<30}")
            self.stdout.write("-" * 100)
            
            for offer in offers:
                expires = offer.get('date_expires', 'Never')
                if isinstance(expires, str) and len(expires) > 10:
                    # Truncate ISO format to just the date part
                    expires = expires.split('T')[0]
                    
                description = offer.get('description', '')
                if description and len(description) > 30:
                    description = description[:27] + '...'
                    
                self.stdout.write(
                    f"{offer.get('code', 'N/A'):<15} | "
                    f"{offer.get('amount', 0):<8} | "
                    f"{offer.get('discount_type', 'N/A'):<12} | "
                    f"{expires:<20} | "
                    f"{description:<30}"
                )

    def _convert_csv_types(self, row):
        """Convert CSV string values to appropriate types"""
        converted = {}
        
        for key, value in row.items():
            if not value:  # Skip empty values
                continue
                
            # Convert common fields to their appropriate types
            if key == 'id':
                converted[key] = int(value)
            elif key in ['amount', 'minimum_amount', 'maximum_amount']:
                converted[key] = float(value)
            elif key in ['usage_count', 'usage_limit', 'usage_limit_per_user', 'limit_usage_to_x_items']:
                if value:  # Only convert if not empty
                    converted[key] = int(value)
            elif key in ['individual_use', 'free_shipping', 'exclude_sale_items']:
                converted[key] = value.lower() in ['true', 'yes', '1']
            elif key in ['product_ids', 'excluded_product_ids', 'product_categories', 
                        'excluded_product_categories', 'email_restrictions', 'used_by']:
                # Convert comma-separated lists
                if value:
                    converted[key] = [item.strip() for item in value.split(',')]
            else:
                # Keep other values as strings
                converted[key] = value
                
        return converted 