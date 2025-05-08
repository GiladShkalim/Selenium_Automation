#!/usr/bin/env python
"""
Database Update Script for IntelliShop

This script updates the MongoDB database with sample data from JSON and CSV files.
It should be run after build.sh when passing the parameter "1".
"""

import os
import sys
import json
import csv
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DatabaseUpdate")

# Add the project directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'mysite'))

# Try to import Django settings
try:
    import django
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()
    
    # Import models after Django setup
    from intellishop.models.mongodb_models import Coupon, Product, User
    from intellishop.utils.mongodb_utils import get_db_handle
except ImportError as e:
    logger.error(f"Failed to import Django modules: {e}")
    sys.exit(1)

def test_mongodb_connection():
    """Test the MongoDB connection before proceeding"""
    try:
        db, client = get_db_handle()
        server_info = client.server_info()
        logger.info(f"Successfully connected to MongoDB version: {server_info['version']}")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()

def find_data_files():
    """Find all JSON and CSV files in the data directory and its subdirectories"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'mysite', 'intellishop', 'data')
    
    json_files = []
    csv_files = []
    
    if not os.path.exists(data_dir):
        logger.warning(f"Data directory not found: {data_dir}")
        return json_files, csv_files
    
    logger.info(f"Scanning for data files in {data_dir}")
    
    # Walk through directory and its subdirectories
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.json'):
                json_files.append(file_path)
            elif file.lower().endswith('.csv'):
                csv_files.append(file_path)
    
    logger.info(f"Found {len(json_files)} JSON files and {len(csv_files)} CSV files")
    
    return json_files, csv_files

def import_json_file(file_path):
    """Import data from a JSON file"""
    try:
        logger.info(f"Importing data from JSON file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both arrays and single objects
        if isinstance(data, dict):
            data = [data]  # Convert to list if it's a single object
        
        if not isinstance(data, list):
            logger.warning(f"Invalid JSON format in {file_path}. Expected a list or object.")
            return False
        
        # Check if this looks like coupon data
        if data and all('code' in item for item in data[:5]):  # Check first 5 items
            logger.info(f"Identified {file_path} as coupon data")
            results = Coupon.import_from_json(data)
            
            logger.info(f"JSON Import results: Total: {results.get('total', 0)}, "
                       f"Valid: {results.get('valid', 0)}, "
                       f"Invalid: {results.get('invalid', 0)}, "
                       f"Updated: {results.get('updated', 0)}, "
                       f"New: {results.get('new', 0)}")
            
            if results.get("errors"):
                logger.warning("Import errors:")
                for error in results["errors"][:10]:  # Show only first 10 errors
                    logger.warning(f"  - {error}")
                
                if len(results["errors"]) > 10:
                    logger.warning(f"  ... and {len(results['errors']) - 10} more errors")
            
            return True
        else:
            logger.warning(f"Unknown data format in {file_path}. Skipping.")
            return False
            
    except Exception as e:
        logger.error(f"Error importing data from JSON file {file_path}: {e}")
        return False

def import_csv_file(file_path):
    """Import data from a CSV file"""
    try:
        logger.info(f"Importing data from CSV file: {file_path}")
        
        # Try to detect if this is a coupon/offer file by checking headers
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip().lower()
            
        # Check if headers match expected coupon fields
        coupon_indicators = ['code', 'amount', 'discount_type']
        is_coupon_file = all(indicator in first_line for indicator in coupon_indicators)
        
        if is_coupon_file:
            logger.info(f"Identified {file_path} as coupon/offer data")
            results = Coupon.import_from_csv(file_path)
            
            logger.info(f"CSV Import results: Total: {results.get('total', 0)}, "
                       f"Valid: {results.get('valid', 0)}, "
                       f"Invalid: {results.get('invalid', 0)}, "
                       f"Updated: {results.get('updated', 0)}, "
                       f"New: {results.get('new', 0)}")
            
            if results.get("errors"):
                logger.warning("Import errors:")
                for error in results["errors"][:10]:  # Show only first 10 errors
                    logger.warning(f"  - {error}")
                
                if len(results["errors"]) > 10:
                    logger.warning(f"  ... and {len(results['errors']) - 10} more errors")
                    
            return True
        else:
            logger.warning(f"Unknown CSV format in {file_path}. Skipping.")
            return False
            
    except Exception as e:
        logger.error(f"Error importing data from CSV file {file_path}: {e}")
        return False

def verify_database_content():
    """Verify the imported content"""
    try:
        # Count items in collections
        coupons_count = Coupon.count()
        products_count = Product.count() if hasattr(Product, 'count') else 0
        users_count = User.count() if hasattr(User, 'count') else 0
        
        logger.info(f"Database verification: {coupons_count} coupons, "
                   f"{products_count} products, {users_count} users")
        
        # Get some stats about coupons
        active_coupons = 0
        expired_coupons = 0
        current_date = datetime.now().isoformat()
        
        coupons = list(Coupon.find({}))
        for coupon in coupons:
            if 'date_expires' in coupon and coupon['date_expires'] and coupon['date_expires'] < current_date:
                expired_coupons += 1
            else:
                active_coupons += 1
        
        logger.info(f"Coupon stats: {active_coupons} active, {expired_coupons} expired")
        return True
    except Exception as e:
        logger.error(f"Error verifying database content: {e}")
        return False

def main():
    """Main function to update the database"""
    logger.info("Starting database update process")
    
    # Test MongoDB connection
    if not test_mongodb_connection():
        logger.error("MongoDB connection test failed. Aborting update.")
        return False
    
    # Find all data files
    json_files, csv_files = find_data_files()
    
    if not json_files and not csv_files:
        logger.warning("No data files found to import. Check your data directory structure.")
        return False
    
    # Process all JSON files
    json_success = True
    for json_file in json_files:
        file_result = import_json_file(json_file)
        json_success = json_success and file_result
    
    # Process all CSV files
    csv_success = True
    for csv_file in csv_files:
        file_result = import_csv_file(csv_file)
        csv_success = csv_success and file_result
    
    # Verify database content
    verify_result = verify_database_content()
    
    if json_success and csv_success and verify_result:
        logger.info("✅ Database update completed successfully!")
        return True
    else:
        logger.warning("⚠️ Database update completed with warnings or errors.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
