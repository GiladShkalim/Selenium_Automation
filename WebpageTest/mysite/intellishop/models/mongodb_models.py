from bson import ObjectId
import datetime
import logging
from jsonschema import validate, ValidationError
import json
import csv

# Constants moved from External-Groq/constants.py
# Categories for coupons
CATEGORIES = [
    "Consumerism", "Travel and Vacation", "Culture and Leisure", 
    "Cars", "Insurance", "Finance and Banking"
]

# Consumer statuses
CONSUMER_STATUS = [
    "Young", "Senior", "Homeowner", "Traveler", "Tech", 
    "Pets", "Fitness", "Student", "Remote", "Family"
]

# Discount types
DISCOUNT_TYPE = [
    "fixed_amount", "percentage", "buy_one_get_one", "Cost"
]

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

# Updated Coupon model with new schema
class Coupon(MongoDBModel):
    collection_name = 'coupons'
    
    # Define the updated coupon schema
    schema = {
        "type": "object",
        "properties": {
            "discount_id": {
                "type": ["string", "null"],
                "description": "Unique automatic identifier of the coupon by MongoDB."
            },
            "title": {
                "type": "string",
                "description": "Title of the coupon."
            },
            "price": {
                "type": "integer",
                "minimum": 0,
                "description": "Price or discount amount."
            },
            "discount_type": {
                "type": "string",
                "enum": DISCOUNT_TYPE,
                "description": "Type of discount (fixed_amount, percentage, buy_one_get_one, Cost)."
            },
            "description": {
                "type": "string",
                "description": "Detailed description of the coupon."
            },
            "image_link": {
                "type": "string",
                "description": "URL to an image representing the coupon."
            },
            "discount_link": {
                "type": "string",
                "description": "URL to the discount page."
            },
            "terms_and_conditions": {
                "type": "string",
                "description": "Terms and conditions for using the coupon."
            },
            "club_name": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of club names associated with the coupon."
            },
            "category": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": CATEGORIES
                },
                "description": "Categories the coupon belongs to."
            },
            "valid_until": {
                "type": "string",
                "description": "Expiry date of the coupon in ISO format."
            },
            "usage_limit": {
                "type": ["integer", "null"],
                "minimum": 1,
                "description": "Total number of times the coupon can be used."
            },
            "coupon_code": {
                "type": "string",
                "description": "Code to be used when redeeming the coupon."
            },
            "provider_link": {
                "type": "string",
                "description": "URL to the provider's website."
            },
            "consumer_statuses": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": CONSUMER_STATUS
                },
                "description": "Consumer statuses this coupon targets."
            }
        },
        "required": ["title", "price", "discount_link"],
        "additionalProperties": True
    }
    
    @classmethod
    def get_all(cls):
        """Get all coupons in the collection"""
        return list(cls.find({}))
    
    @classmethod
    def get_by_code(cls, code):
        """Get a coupon by its code"""
        return cls.find_one({'coupon_code': code})
    
    @classmethod
    def get_active_coupons(cls):
        """Get all active coupons (not expired)"""
        current_date = datetime.datetime.utcnow().isoformat()
        return cls.find({
            '$or': [
                {'valid_until': {'$exists': False}},
                {'valid_until': None},
                {'valid_until': ''},
                {'valid_until': {'$gt': current_date}}
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
        
        try:
            # Check if the data is a list of coupons or a single coupon
            coupons_data = json_data if isinstance(json_data, list) else [json_data]
            
            for coupon_data in coupons_data:
                results['total'] += 1
                
                try:
                    # Normalize and set defaults for the coupon data
                    coupon = cls._normalize_coupon_data(coupon_data)
                    
                    # Validate against schema
                    try:
                        validate(instance=coupon, schema=cls.schema)
                    except ValidationError as e:
                        results['invalid'] += 1
                        results['errors'].append(f"Coupon {coupon.get('coupon_code', coupon.get('title', 'unknown'))}: {str(e)}")
                        continue
                    
                    # Check if we want to update by coupon_code (if it exists)
                    if 'coupon_code' in coupon and coupon['coupon_code']:
                        existing = cls.find_one({'coupon_code': coupon['coupon_code']})
                        
                        if existing:
                            # Update existing coupon
                            cls.update_one({'_id': existing['_id']}, coupon)
                            results['updated'] += 1
                        else:
                            # Insert new coupon
                            cls.insert_one(coupon)
                            results['new'] += 1
                    else:
                        # Insert as new coupon
                        cls.insert_one(coupon)
                        results['new'] += 1
                        
                    results['valid'] += 1
                    
                except Exception as e:
                    results['invalid'] += 1
                    results['errors'].append(f"Coupon {coupon_data.get('coupon_code', coupon_data.get('title', 'unknown'))}: {str(e)}")
        
        except Exception as e:
            results['errors'].append(f"JSON processing error: {str(e)}")
            
        return results
    
    @classmethod
    def _normalize_coupon_data(cls, coupon_data):
        """Normalize coupon data to match schema requirements"""
        coupon = dict(coupon_data)  # Create a copy to avoid modifying the original
        
        # Set default values for required fields if missing
        if 'title' not in coupon or not coupon['title']:
            coupon['title'] = ""
            
        if 'price' not in coupon:
            coupon['price'] = 0
        elif isinstance(coupon['price'], dict) and 'amount' in coupon['price']:
            # Handle price objects (legacy format)
            coupon['price'] = int(coupon['price']['amount'])
        elif not isinstance(coupon['price'], int):
            # Try to convert string or other types to integer
            try:
                # Remove any currency symbols or non-numeric chars except decimal point
                price_str = str(coupon['price']).replace('%', '').strip()
                coupon['price'] = int(float(price_str))
            except ValueError:
                coupon['price'] = 0
        
        if 'discount_link' not in coupon:
            coupon['discount_link'] = ""
            
        # Set defaults for optional fields
        if 'description' not in coupon:
            coupon['description'] = "[No description provided]"
            
        if 'image_link' not in coupon:
            coupon['image_link'] = ""
            
        if 'terms_and_conditions' not in coupon:
            coupon['terms_and_conditions'] = "See provider website for details"
            
        if 'club_name' not in coupon:
            coupon['club_name'] = []
        elif isinstance(coupon['club_name'], str):
            coupon['club_name'] = [coupon['club_name']]
            
        if 'category' not in coupon:
            coupon['category'] = []
        elif isinstance(coupon['category'], str):
            coupon['category'] = [coupon['category']]
            
        if 'valid_until' not in coupon:
            coupon['valid_until'] = ""
            
        if 'usage_limit' not in coupon:
            coupon['usage_limit'] = 1
            
        if 'coupon_code' not in coupon:
            coupon['coupon_code'] = ""
            
        if 'provider_link' not in coupon:
            coupon['provider_link'] = ""
            
        if 'consumer_statuses' not in coupon:
            coupon['consumer_statuses'] = []
        elif isinstance(coupon['consumer_statuses'], str):
            coupon['consumer_statuses'] = [coupon['consumer_statuses']]
        
        # Infer discount_type if not provided
        if 'discount_type' not in coupon:
            price_str = str(coupon_data.get('price', ''))
            if '%' in price_str:
                coupon['discount_type'] = 'percentage'
            else:
                coupon['discount_type'] = 'fixed_amount'
        
        return coupon

    @classmethod
    def import_from_csv(cls, csv_file):
        """Import coupons from a CSV file or file object"""
        results = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'updated': 0,
            'new': 0,
            'errors': []
        }
        
        close_after = False
        
        try:
            # If a string path is provided, open the file
            if isinstance(csv_file, str):
                file_obj = open(csv_file, 'r', encoding='utf-8')
                close_after = True
            else:
                file_obj = csv_file
                
            try:
                # Read the CSV file
                reader = csv.DictReader(file_obj)
                if not reader.fieldnames:
                    results['errors'].append("CSV file has no headers")
                    return results
                    
                # Map CSV fields to model fields (case insensitive)
                field_mapping = {
                    'id': 'discount_id',
                    'discount_id': 'discount_id',
                    'title': 'title',
                    'name': 'title',
                    'price': 'price',
                    'amount': 'price',
                    'discount': 'price',
                    'discount_type': 'discount_type',
                    'price_type': 'discount_type',
                    'type': 'discount_type',
                    'description': 'description',
                    'desc': 'description',
                    'image': 'image_link',
                    'image_link': 'image_link',
                    'image_url': 'image_link',
                    'link': 'discount_link',
                    'discount_link': 'discount_link',
                    'url': 'discount_link',
                    'terms': 'terms_and_conditions',
                    'terms_and_conditions': 'terms_and_conditions',
                    'tc': 'terms_and_conditions',
                    'club': 'club_name',
                    'club_name': 'club_name',
                    'category': 'category',
                    'categories': 'category',
                    'valid_until': 'valid_until',
                    'expiry': 'valid_until',
                    'expiry_date': 'valid_until',
                    'expires': 'valid_until',
                    'usage_limit': 'usage_limit',
                    'limit': 'usage_limit',
                    'code': 'coupon_code',
                    'coupon_code': 'coupon_code',
                    'provider': 'provider_link',
                    'provider_link': 'provider_link',
                    'provider_url': 'provider_link',
                    'consumer_status': 'consumer_statuses',
                    'consumer_statuses': 'consumer_statuses',
                    'status': 'consumer_statuses'
                }
                
                for row in reader:
                    results['total'] += 1
                    
                    try:
                        # Map CSV fields to model fields
                        coupon = {}
                        for csv_field, value in row.items():
                            if csv_field.lower() in field_mapping:
                                model_field = field_mapping[csv_field.lower()]
                                
                                # Handle array fields
                                if model_field in ['category', 'club_name', 'consumer_statuses']:
                                    if value:
                                        coupon[model_field] = [v.strip() for v in value.split(',')]
                                else:
                                    coupon[model_field] = value
                        
                        # Normalize and set defaults
                        coupon = cls._normalize_coupon_data(coupon)
                        
                        # Validate against schema
                        try:
                            validate(instance=coupon, schema=cls.schema)
                        except ValidationError as e:
                            results['invalid'] += 1
                            results['errors'].append(f"Row {results['total']}: {str(e)}")
                            continue
                        
                        # Check if we want to update by coupon_code (if it exists)
                        if 'coupon_code' in coupon and coupon['coupon_code']:
                            existing = cls.find_one({'coupon_code': coupon['coupon_code']})
                            
                            if existing:
                                # Update existing coupon
                                cls.update_one({'_id': existing['_id']}, coupon)
                                results['updated'] += 1
                            else:
                                # Insert new coupon
                                cls.insert_one(coupon)
                                results['new'] += 1
                        else:
                            # Insert as new coupon
                            cls.insert_one(coupon)
                            results['new'] += 1
                            
                        results['valid'] += 1
                        
                    except Exception as e:
                        results['invalid'] += 1
                        results['errors'].append(f"Row {results['total']}: {str(e)}")
                        
            finally:
                if close_after:
                    file_obj.close()
                    
        except Exception as e:
            results['errors'].append(f"CSV processing error: {str(e)}")
            
        return results