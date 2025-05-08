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
            "discount_id": {
                "type": ["string", "null"],
                "description": "Unique automatic identifier of the coupon by MongoDB."
            },
            "title": {
                "type": "string",
                "description": "Name or title of the coupon.",
            },
            "price": {
                "type": ["number", "string"],
                "description": "Discount amount (can be numeric or percentage)."
            },
            "price_type": {
                "type": "string",
                "enum": ["fixed_amount", "percentage", "buy_one_get_one", "Cost"],
                "description": "Type of discount offered."
            },
            "description": {
                "type": ["string", "null"],
                "description": "Detailed description of the coupon."
            },
            "image_link": {
                "type": ["string", "null"],
                "description": "Link to an image representing the coupon."
            },
            "discount_link": {
                "type": "string",
                "description": "Link to the original offer or product page."
            },
            "terms_and_conditions": {
                "type": ["string", "null"],
                "description": "Terms and conditions or restrictions related to the coupon."
            },
            "club_name": {
                "type": ["string", "null"],
                "enum": [
                    "Young", "Senior", "Homeowner", "Traveler", 
                    "Tech", "Pets", "Fitness", "Student", 
                    "Remote", "Family", None
                ],
                "description": "Club name associated with the coupon."
            },
            "category": {
                "type": ["array", "string", "null"],
                "items": {
                    "type": "string",
                    "enum": [
                        "Consumerism", "Travel and Vacation", 
                        "Culture and Leisure", "Cars", 
                        "Insurance", "Finance and Banking"
                    ]
                },
                "description": "Categories the coupon belongs to."
            },
            "valid_until": {
                "type": "string",
                "description": "Expiry date of the coupon in ISO format."
            },
            "usage_limit": {
                "type": ["integer", "null"],
                "description": "Total number of times the coupon can be used."
            },
            "usage_count": {
                "type": ["integer", "null"],
                "description": "Number of times the coupon has been used."
            },
            "coupon_code": {
                "type": "string",
                "description": "Unique code to identify the coupon."
            }
        },
        "required": ["title", "price", "discount_link", "valid_until", "coupon_code"]
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
                {'valid_until': {'$gt': current_date}}
            ]
        })
    
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
        
        try:
            # Check if we got a file path or a file object
            if isinstance(csv_file, str):
                # If it's a string (file path), open the file
                file_obj = open(csv_file, 'r', encoding='utf-8')
                should_close = True
            else:
                # If it's already a file object, use it directly
                file_obj = csv_file
                should_close = False
            
            try:
                csv_reader = csv.DictReader(file_obj)
                
                for row in csv_reader:
                    results['total'] += 1
                    
                    try:
                        coupon = {}
                        
                        # Process fields, handling missing values
                        for field, value in row.items():
                            if field and value is not None:  # Modified check - allow zero values but not None
                                field = field.strip()
                                # For string values, strip whitespace
                                if isinstance(value, str):
                                    value = value.strip()
                                
                                # Handle field name mapping (for compatibility)
                                if field == 'discount_type':
                                    field = 'price_type'
                                    
                                if field in ['price', 'usage_limit', 'usage_count']:
                                    try:
                                        # Convert to number but allow zero values
                                        coupon[field] = int(value)
                                    except ValueError:
                                        # Try to parse as float if it has decimal point
                                        if isinstance(value, str) and '.' in value:
                                            coupon[field] = float(value)
                                        else:
                                            coupon[field] = value
                                elif field == 'category' and isinstance(value, str) and ',' in value:
                                    # Split categories into an array
                                    coupon[field] = [cat.strip() for cat in value.split(',')]
                                elif field == 'club_name' and isinstance(value, str) and ',' in value:
                                    # Split club_name into an array if it contains commas
                                    coupon[field] = [club.strip() for club in value.split(',')]
                                else:
                                    coupon[field] = value
                        
                        # Map discount_type to price_type if needed
                        if 'discount_type' in coupon and 'price_type' not in coupon:
                            coupon['price_type'] = coupon.pop('discount_type')
                        
                        # Validate required fields - consider 0 as a valid value for price
                        required_fields = ['title', 'discount_link', 'coupon_code']
                        # Special check for price field to allow 0 values
                        if 'price' not in coupon and coupon.get('price', None) != 0:
                            required_fields.append('price')
                        
                        missing_fields = [field for field in required_fields if field not in coupon or (coupon[field] == "" and field != 'price')]
                        if missing_fields:
                            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
                        
                        # Set defaults for missing fields
                        if 'description' not in coupon:
                            coupon['description'] = f"Discount offer: {coupon['title']}"
                        
                        if 'price_type' not in coupon:
                            # Infer price_type from price
                            price = str(coupon['price'])
                            if '%' in price:
                                coupon['price_type'] = 'percentage'
                                # Extract numeric value if price contains %
                                coupon['price'] = float(price.replace('%', '').strip())
                            elif price.lower() in ['buy_one_get_one', 'bogo']:
                                coupon['price_type'] = 'buy_one_get_one'
                            elif price.lower() in ['free_shipping', 'shipping', 'free shipping']:
                                coupon['price_type'] = 'Cost'
                            else:
                                coupon['price_type'] = 'fixed_amount'
                        
                        if 'terms_and_conditions' not in coupon:
                            coupon['terms_and_conditions'] = "See provider website for details"
                        
                        if 'club_name' not in coupon:
                            coupon['club_name'] = None
                        
                        if 'category' not in coupon:
                            coupon['category'] = ["Consumerism"]
                        
                        # Handle date format for valid_until
                        if 'valid_until' in coupon and coupon['valid_until']:
                            # Keep as string for ISO format compatibility
                            if 'T' not in coupon['valid_until'] and len(coupon['valid_until']) == 10:
                                # If it's just a date without time, add time
                                coupon['valid_until'] = f"{coupon['valid_until']}T23:59:59"
                        
                        # Handle usage_limit if not present
                        if 'usage_limit' not in coupon:
                            coupon['usage_limit'] = 0  # unlimited
                        
                        # Check for existing coupon with same code
                        existing_coupon = cls.find_one({'coupon_code': coupon['coupon_code']})
                        
                        if existing_coupon:
                            coupon_id = existing_coupon['_id']
                            # Merge with existing coupon data, keeping the new values
                            merged_coupon = {**existing_coupon, **coupon}
                            cls.update_one({'_id': coupon_id}, merged_coupon)
                            results['updated'] += 1
                        else:
                            # Insert new coupon
                            cls.insert_one(coupon)
                            results['new'] += 1
                            
                        results['valid'] += 1
                        
                    except Exception as e:
                        results['invalid'] += 1
                        results['errors'].append(f"Coupon {row.get('coupon_code', 'unknown')}: {str(e)}")
            finally:
                if should_close:
                    file_obj.close()
                    
        except Exception as e:
            results['errors'].append(f"CSV processing error: {str(e)}")
            
        return results

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
            if not isinstance(json_data, list):
                json_data = [json_data]
                
            for coupon_data in json_data:
                results['total'] += 1
                
                try:
                    # Validate and prepare coupon data
                    coupon = {}
                    
                    # Extract fields from JSON
                    for field, value in coupon_data.items():
                        if field == 'discount_type':
                            # Map legacy discount_type to price_type
                            discount_type = value.lower()
                            if discount_type == 'percent' or discount_type == 'percentage':
                                coupon['price_type'] = 'percentage'
                            elif discount_type == 'fixed_cart' or discount_type == 'fixed_amount':
                                coupon['price_type'] = 'fixed_amount'
                            else:
                                coupon['price_type'] = discount_type
                        elif field == 'code':
                            # Map legacy code field to coupon_code
                            coupon['coupon_code'] = value
                        elif field == 'amount':
                            # Map legacy amount field to price
                            coupon['price'] = value
                        elif field == 'date_expires':
                            # Map legacy date_expires to valid_until
                            coupon['valid_until'] = value
                        else:
                            coupon[field] = value
                    
                    # Validate required fields
                    required_fields = ['title', 'price', 'discount_link', 'coupon_code']
                    for field in required_fields:
                        if field not in coupon or not coupon[field]:
                            raise ValueError(f"Missing required field: {field}")
                    
                    # Set defaults for missing fields
                    if 'description' not in coupon:
                        coupon['description'] = "[No description provided]"
                        
                    if 'price_type' not in coupon:
                        # Infer price_type from price
                        price = str(coupon['price'])
                        if '%' in price:
                            coupon['price_type'] = 'percentage'
                        else:
                            coupon['price_type'] = 'fixed_amount'
                    
                    if 'terms_and_conditions' not in coupon:
                        coupon['terms_and_conditions'] = "See provider website for details"
                    
                    if 'club_name' not in coupon:
                        coupon['club_name'] = "[Unknown Club]"
                    
                    if 'category' not in coupon:
                        coupon['category'] = "Uncategorized"
                    
                    # Check for existing coupon with same code
                    coupon_id = None
                    existing_coupon = cls.find_one({'coupon_code': coupon['coupon_code']})
                    
                    if existing_coupon:
                        coupon_id = existing_coupon['_id']
                        # Merge with existing coupon data, keeping the new values
                        merged_coupon = {**existing_coupon, **coupon}
                        cls.update_one({'_id': coupon_id}, merged_coupon)
                        results['updated'] += 1
                    else:
                        # Insert new coupon
                        cls.insert_one(coupon)
                        results['new'] += 1
                        
                    results['valid'] += 1
                    
                except Exception as e:
                    results['invalid'] += 1
                    results['errors'].append(f"Coupon {coupon_data.get('coupon_code', coupon_data.get('code', 'unknown'))}: {str(e)}")
        
        except Exception as e:
            results['errors'].append(f"JSON processing error: {str(e)}")
            
        return results