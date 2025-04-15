from bson import ObjectId

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
        return cls.get_collection().find_one(query)
    
    @classmethod
    def find(cls, query=None, sort=None, limit=None):
        """Find multiple documents"""
        cursor = cls.get_collection().find(query or {})
        
        if sort:
            cursor = cursor.sort(sort)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    @classmethod
    def insert_one(cls, document):
        """Insert a document into the collection"""
        result = cls.get_collection().insert_one(document)
        return result.inserted_id
    
    @classmethod
    def update_one(cls, query, update):
        """Update a document in the collection"""
        return cls.get_collection().update_one(query, {'$set': update})
    
    @classmethod
    def delete_one(cls, query):
        """Delete a document from the collection"""
        return cls.get_collection().delete_one(query)

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