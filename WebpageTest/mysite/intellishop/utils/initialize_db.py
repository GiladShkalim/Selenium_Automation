from intellishop.utils.mongodb_utils import get_collection_handle
import logging

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

def initialize_database():
    """Initialize MongoDB database with required setup"""
    try:
        create_indexes()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
    # Add any other initialization tasks here 