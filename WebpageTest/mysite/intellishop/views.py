# View functions that handle HTTP requests and return responses
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models.mongodb_models import Product, User
import json
from pymongo.errors import DuplicateKeyError

def index(request):
    return render(request, 'intellishop/index.html')

def index_home(request):
    return render(request, 'intellishop/index_home_original.html')

def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.find_one({
                'email': data['email'], 
                'password': data['password']
            })
            
            if user is not None:
                # In production, use Django session framework properly
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful',
                    'redirect': '/dashboard/',
                    'user_id': str(user['_id'])
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid credentials'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
            
    return render(request, 'intellishop/login.html')

def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Check if user already exists - with explicit None check
            existing_user = User.get_by_username(data['username'])
            if existing_user is not None:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username already exists'
                }, status=400)
            
            existing_email = User.get_by_email(data['email'])
            if existing_email is not None:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already exists'
                }, status=400)
            
            # Create new user in MongoDB
            user_id = User.create_user(
                username=data['username'],
                password=data['password'],  # In production, hash the password
                email=data['email'],
                status=data['status'],
                age=data['age'],
                location=data['location'],
                hobbies=data['hobbies']
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'User registered successfully',
                'user_id': str(user_id)
            })
            
        except DuplicateKeyError:
            return JsonResponse({
                'status': 'error', 
                'message': 'Username or email already exists'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=400)
    
    return render(request, 'intellishop/register.html')

def dashboard(request):
    # Get all users from MongoDB
    users = User.find()
    
    # Convert MongoDB ObjectId to string for template
    for user in users:
        if user is not None and '_id' in user:
            user['_id'] = str(user['_id'])
    
    return render(request, 'intellishop/dashboard.html', {'users': users})

def template(request):
    return render(request, 'intellishop/Site_template.html')

def product_list(request):
    """View to list products, optionally filtered by category"""
    category = request.GET.get('category', None)
    
    if category:
        products = Product.get_by_category(category)
    else:
        products = Product.find()
    
    # Convert ObjectId to string for JSON serialization
    for product in products:
        if product and '_id' in product:
            product['_id'] = str(product['_id'])
    
    return JsonResponse({'products': products})

def product_detail(request, product_id):
    """View to display a specific product"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # Convert ObjectId to string for JSON serialization
    product['_id'] = str(product['_id'])
    
    return JsonResponse({'product': product})

def aliexpress_coupons(request):
    return render(request, 'intellishop/coupon_for_aliexpress.html') 