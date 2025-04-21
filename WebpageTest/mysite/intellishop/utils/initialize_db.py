from intellishop.utils.mongodb_utils import get_collection_handle
from intellishop.models.mongodb_models import Coupon
import logging
import os
import csv
import json

logger = logging.getLogger(__name__)

def create_indexes():
    """Create MongoDB indexes for performance and constraints"""
    # Users collection
    users_collection = get_collection_handle('users')
    
    # Add None check before trying to create indexes
    if users_collection is not None:
        try:
            # Create unique indexes
            users_collection.create_index('username', unique=True)
            users_collection.create_index('email', unique=True)
            logger.info("Created user collection indexes")
        except Exception as e:
            logger.error(f"Error creating user indexes: {str(e)}")
    else:
        logger.error("Could not get users collection handle")
    
    # Products collection
    products_collection = get_collection_handle('products')
    
    # Add None check before trying to create indexes
    if products_collection is not None:
        try:
            products_collection.create_index('category')
            logger.info("Created product collection indexes")
        except Exception as e:
            logger.error(f"Error creating product indexes: {str(e)}")
    else:
        logger.error("Could not get products collection handle")
        
    # Coupons collection
    coupons_collection = get_collection_handle('coupons')
    
    # Add None check before trying to create indexes
    if coupons_collection is not None:
        try:
            # Create unique index on coupon code
            coupons_collection.create_index('code', unique=True)
            # Create index for finding active coupons
            coupons_collection.create_index('date_expires')
            logger.info("Created coupon collection indexes")
        except Exception as e:
            logger.error(f"Error creating coupon indexes: {str(e)}")
    else:
        logger.error("Could not get coupons collection handle")

def import_sample_coupon_data():
    """Import sample coupon data from JSON and CSV files in the data directory"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data', 'coupons')
        
        if not os.path.exists(data_dir):
            logger.warning(f"Coupon data directory not found: {data_dir}")
            # Try finding data in the parent app directory
            data_dir = os.path.join(base_dir, 'data')
            if not os.path.exists(data_dir):
                logger.warning(f"No data directory found at: {data_dir}")
                return
        
        files_processed = 0
        total_valid = 0
        
        # Process JSON files
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        for json_file in json_files:
            file_path = os.path.join(data_dir, json_file)
            try:
                logger.info(f"Importing coupons from JSON file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                result = Coupon.import_from_json(json_data)
                files_processed += 1
                total_valid += result['valid']
                logger.info(f"Processed {result['total']} coupons from {json_file}: {result['valid']} valid, {result['invalid']} invalid")
            except Exception as e:
                logger.error(f"Error importing from JSON file {json_file}: {str(e)}")
        
        # Process CSV files
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        for csv_file in csv_files:
            file_path = os.path.join(data_dir, csv_file)
            try:
                logger.info(f"Importing coupons from CSV file: {file_path}")
                result = Coupon.import_from_csv(file_path)
                files_processed += 1
                total_valid += result['valid']
                logger.info(f"Processed {result['total']} coupons from {csv_file}: {result['valid']} valid, {result['invalid']} invalid")
            except Exception as e:
                logger.error(f"Error importing from CSV file {csv_file}: {str(e)}")
                
        if files_processed > 0:
            logger.info(f"Successfully imported {total_valid} coupons from {files_processed} files")
        else:
            logger.warning("No coupon data files found to import")
    
    except Exception as e:
        logger.error(f"Error during coupon data import: {str(e)}")

def initialize_database():
    """Initialize MongoDB database with required setup"""
    try:
        create_indexes()
        import_sample_coupon_data()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
    # Add any other initialization tasks here 