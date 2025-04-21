from bson import ObjectId
import datetime
import logging
from jsonschema import validate, ValidationError
import json
import csv

logger = logging.getLogger(__name__)

class MongoDBModel:
    """Base class for MongoDB models"""
    collection_name = None
    
    @classmethod
    def get_collection(cls):
        """Get the MongoDB collection for this model"""
        from intellishop.utils.mongodb_utils import get_collection_handle
        return get_collection_handle(cls.collection_name)
    
    @classmethod
    def find_one(cls, query):
        """Find a single document"""
        collection = cls.get_collection()
        if collection is not None:  # Add explicit None check
            return collection.find_one(query)
        return None
    
    @classmethod
    def find(cls, query=None, sort=None, limit=None):
        """Find multiple documents"""
        collection = cls.get_collection()
        if collection is not None:  # Add explicit None check
            cursor = collection.find(query or {})
            
            if sort:
                cursor = cursor.sort(sort)
            
            if limit:
                cursor = cursor.limit(limit)
            
            return list(cursor)
        return []  # Return empty list instead of None for consistency
    
    @classmethod
    def insert_one(cls, document):
        """Insert a document into the collection"""
        collection = cls.get_collection()
        if collection is not None:  # Add explicit None check
            result = collection.insert_one(document)
            return result.inserted_id
        return None
    
    @classmethod
    def update_one(cls, query, update):
        """Update a document in the collection"""
        collection = cls.get_collection()
        if collection is not None:  # Add explicit None check
            return collection.update_one(query, {'$set': update})
        return None
    
    @classmethod
    def delete_one(cls, query):
        """Delete a document from the collection"""
        collection = cls.get_collection()
        if collection is not None:  # Add explicit None check
            return collection.delete_one(query)
        return None

# Example model for product data
class Product(MongoDBModel):
    collection_name = 'products'
    
    @classmethod
    def create_product(cls, name, description, price, category, image_url=None):
        """Create a new product"""
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'category': category,
            'image_url': image_url
        }
        return cls.insert_one(product_data)
    
    @classmethod
    def get_by_category(cls, category):
        """Get products by category"""
        return cls.find({'category': category})
    
    @classmethod
    def get_by_id(cls, product_id):
        """Get a product by its ID"""
        return cls.find_one({'_id': ObjectId(product_id)})

# Add this User model for MongoDB
class User(MongoDBModel):
    collection_name = 'users'
    
    @classmethod
    def create_user(cls, username, password, email, status, age, location, hobbies):
        """Create a new user in MongoDB"""
        user_data = {
            'username': username,
            'password': password,  # In production, hash this password
            'email': email,
            'status': status,
            'age': age,
            'location': location,
            'hobbies': hobbies,
            'created_at': datetime.datetime.now()
        }
        return cls.insert_one(user_data)
    
    @classmethod
    def get_by_username(cls, username):
        """Get a user by username"""
        return cls.find_one({'username': username})
    
    @classmethod
    def get_by_email(cls, email):
        """Get a user by email"""
        return cls.find_one({'email': email})
    
    @classmethod
    def get_by_id(cls, user_id):
        """Get a user by ID"""
        return cls.find_one({'_id': ObjectId(user_id)})

# Add this Coupon model to your MongoDB models
class Coupon(MongoDBModel):
    collection_name = 'coupons'
    
    # Define the coupon schema
    schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
                "description": "Unique identifier for the coupon."
            },
            "code": {
                "type": "string",
                "description": "The code that customers will use to apply the coupon.",
                "pattern": "^[a-zA-Z0-9_]+$"
            },
            "amount": {
                "type": "number",
                "minimum": 0,
                "description": "The amount of discount provided by the coupon."
            },
            "date_created": {
                "type": "string",
                "format": "date-time",
                "description": "The date and time when the coupon was created."
            },
            "date_created_gmt": {
                "type": "string",
                "format": "date-time",
                "description": "The date and time when the coupon was created in GMT."
            },
            "date_modified": {
                "type": "string",
                "format": "date-time",
                "description": "The date and time when the coupon was last modified."
            },
            "date_modified_gmt": {
                "type": "string",
                "format": "date-time",
                "description": "The date and time when the coupon was last modified in GMT."
            },
            "discount_type": {
                "type": "string",
                "enum": ["percent", "fixed_cart", "fixed_product"],
                "description": "The type of discount provided by the coupon."
            },
            "description": {
                "type": ["string", "null"],
                "description": "A brief description of the coupon."
            },
            "date_expires": {
                "type": "string",
                "format": "date-time",
                "description": "The date and time when the coupon expires."
            },
            "date_expires_gmt": {
                "type": "string",
                "format": "date-time",
                "description": "The date and time when the coupon expires in GMT."
            },
            "usage_count": {
                "type": "integer",
                "minimum": 0,
                "description": "The number of times the coupon has been used."
            },
            "individual_use": {
                "type": "boolean",
                "description": "Whether the coupon can be used individually or with other coupons."
            },
            "product_ids": {
                "type": ["array", "null"],
                "items": {
                    "type": "integer"
                },
                "description": "The products to which the coupon applies."
            },
            "excluded_product_ids": {
                "type": ["array", "null"],
                "items": {
                    "type": "integer"
                },
                "description": "The products excluded from the coupon."
            },
            "usage_limit": {
                "type": "integer",
                "minimum": 1,
                "description": "The maximum number of times the coupon can be used."
            },
            "usage_limit_per_user": {
                "type": ["integer", "null"],
                "minimum": 1,
                "description": "The maximum number of times a user can use the coupon."
            },
            "limit_usage_to_x_items": {
                "type": ["integer", "null"],
                "minimum": 1,
                "description": "The maximum number of items the coupon can be applied to."
            },
            "free_shipping": {
                "type": "boolean",
                "description": "Whether the coupon grants free shipping."
            },
            "product_categories": {
                "type": ["array", "null"],
                "items": {
                    "type": "string"
                },
                "description": "The categories to which the coupon applies."
            },
            "excluded_product_categories": {
                "type": ["array", "null"],
                "items": {
                    "type": "string"
                },
                "description": "The categories excluded from the coupon."
            },
            "exclude_sale_items": {
                "type": "boolean",
                "description": "Whether the coupon applies to items on sale."
            },
            "minimum_amount": {
                "type": "number",
                "minimum": 0,
                "description": "The minimum purchase amount required to use the coupon."
            },
            "maximum_amount": {
                "type": "number",
                "minimum": 0,
                "description": "The maximum purchase amount for which the coupon applies."
            },
            "email_restrictions": {
                "type": ["array", "null"],
                "items": {
                    "type": "string",
                    "format": "email"
                },
                "description": "The email addresses restricted from using the coupon."
            },
            "used_by": {
                "type": ["array", "null"],
                "items": {
                    "type": "string"
                },
                "description": "The users who have used the coupon."
            },
            "meta_data": {
                "type": ["array", "null"],
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "key": {"type": "string"},
                        "value": {"type": "string"}
                    },
                    "required": ["id", "key", "value"]
                },
                "description": "Additional metadata associated with the coupon."
            }
        },
        "required": [
            "id", "code", "amount", "discount_type"
        ]
    }
    
    @classmethod
    def validate_coupon(cls, coupon_data):
        """Validate a coupon against the schema"""
        try:
            validate(instance=coupon_data, schema=cls.schema)
            return True, None
        except ValidationError as e:
            return False, str(e)
    
    @classmethod
    def get_by_code(cls, code):
        """Get a coupon by its code"""
        return cls.find_one({'code': code})
    
    @classmethod
    def get_active_coupons(cls):
        """Get all active coupons (not expired)"""
        current_date = datetime.datetime.utcnow().isoformat()
        return cls.find({
            '$or': [
                {'date_expires': {'$exists': False}},
                {'date_expires': None},
                {'date_expires': {'$gt': current_date}}
            ]
        })
    
    @classmethod
    def import_from_json(cls, json_data):
        """Import coupons from JSON data"""
        results = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'updated': 0,
            'new': 0,
            'errors': []
        }
        
        if isinstance(json_data, str):
            try:
                coupons = json.loads(json_data)
            except json.JSONDecodeError as e:
                results['errors'].append(f"Invalid JSON format: {str(e)}")
                return results
        else:
            coupons = json_data
            
        if not isinstance(coupons, list):
            coupons = [coupons]
            
        results['total'] = len(coupons)
            
        for coupon in coupons:
            # Validate coupon against schema
            is_valid, error = cls.validate_coupon(coupon)
            
            if not is_valid:
                results['invalid'] += 1
                results['errors'].append(f"Coupon {coupon.get('code', 'unknown')}: {error}")
                continue
                
            # Check if coupon with same code already exists
            existing_coupon = cls.get_by_code(coupon['code'])
            
            if existing_coupon:
                # Update existing coupon, preserving the MongoDB _id field
                coupon_id = existing_coupon.get('_id')
                # Create a copy of the coupon to avoid modifying the original
                merged_coupon = coupon.copy()
                # Update with new data, but preserve usage statistics if not provided
                if 'usage_count' not in merged_coupon and 'usage_count' in existing_coupon:
                    merged_coupon['usage_count'] = existing_coupon['usage_count']
                if 'used_by' not in merged_coupon and 'used_by' in existing_coupon:
                    merged_coupon['used_by'] = existing_coupon['used_by']
                    
                cls.update_one({'_id': coupon_id}, merged_coupon)
                results['updated'] += 1
            else:
                # Insert new coupon
                cls.insert_one(coupon)
                results['new'] += 1
                
            results['valid'] += 1
            
        return results
    
    @classmethod
    def import_from_csv(cls, csv_file_path):
        """Import coupons from a CSV file"""
        results = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'updated': 0,
            'new': 0,
            'errors': []
        }
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                coupons = list(csv_reader)
                
            results['total'] = len(coupons)
            
            # Process each coupon
            for coupon in coupons:
                # Convert string values to appropriate types
                try:
                    # Convert numeric values
                    if 'id' in coupon:
                        coupon['id'] = int(coupon['id'])
                    if 'amount' in coupon:
                        coupon['amount'] = float(coupon['amount'])
                    if 'usage_count' in coupon:
                        coupon['usage_count'] = int(coupon['usage_count'])
                    if 'usage_limit' in coupon:
                        coupon['usage_limit'] = int(coupon['usage_limit'])
                    if 'minimum_amount' in coupon:
                        coupon['minimum_amount'] = float(coupon['minimum_amount'])
                    if 'maximum_amount' in coupon:
                        coupon['maximum_amount'] = float(coupon['maximum_amount'])
                        
                    # Convert boolean values
                    if 'individual_use' in coupon:
                        coupon['individual_use'] = coupon['individual_use'].lower() == 'true'
                    if 'free_shipping' in coupon:
                        coupon['free_shipping'] = coupon['free_shipping'].lower() == 'true'
                    if 'exclude_sale_items' in coupon:
                        coupon['exclude_sale_items'] = coupon['exclude_sale_items'].lower() == 'true'
                        
                    # Convert list values
                    for list_field in ['product_ids', 'excluded_product_ids', 'product_categories', 
                                      'excluded_product_categories', 'email_restrictions', 'used_by']:
                        if list_field in coupon and coupon[list_field]:
                            if isinstance(coupon[list_field], str):
                                # Assume comma-separated values
                                coupon[list_field] = [item.strip() for item in coupon[list_field].split(',')]
                            
                    # Validate coupon
                    is_valid, error = cls.validate_coupon(coupon)
                    
                    if not is_valid:
                        results['invalid'] += 1
                        results['errors'].append(f"Coupon {coupon.get('code', 'unknown')}: {error}")
                        continue
                        
                    # Check if coupon exists
                    existing_coupon = cls.get_by_code(coupon['code'])
                    
                    if existing_coupon:
                        # Update existing coupon, preserving the MongoDB _id field
                        coupon_id = existing_coupon.get('_id')
                        # Create a copy of the coupon to avoid modifying the original
                        merged_coupon = coupon.copy()
                        # Update with new data, but preserve usage statistics if not provided
                        if 'usage_count' not in merged_coupon and 'usage_count' in existing_coupon:
                            merged_coupon['usage_count'] = existing_coupon['usage_count']
                        if 'used_by' not in merged_coupon and 'used_by' in existing_coupon:
                            merged_coupon['used_by'] = existing_coupon['used_by']
                            
                        cls.update_one({'_id': coupon_id}, merged_coupon)
                        results['updated'] += 1
                    else:
                        # Insert new coupon
                        cls.insert_one(coupon)
                        results['new'] += 1
                        
                    results['valid'] += 1
                    
                except Exception as e:
                    results['invalid'] += 1
                    results['errors'].append(f"Coupon {coupon.get('code', 'unknown')}: {str(e)}")
                    
        except Exception as e:
            results['errors'].append(f"CSV processing error: {str(e)}")
            
        return results 