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
            print("\n=== FULL DEBUG ===")
            print("Attempting login with:", data)
            
            # Find user and print raw result
            collection = User.get_collection()
            raw_user = collection.find_one({'email': data['email']})
            print("Raw MongoDB result:", raw_user)
            
            user = User.find_one({'email': data['email']})
            print("User object:", user)
            
            print("=== Login Debug ===")
            print("1. Login attempt with email:", data['email'])
            print("2. Provided password:", data['password'])
            
            # Find user by email only first
            if user:
                print("4. User details:", {
                    'username': user.get('username'),
                    'email': user.get('email'),
                    'password': user.get('password'),
                    'status': user.get('status')
                })
                
                stored_password = user.get('password', '')
                input_password = data.get('password', '')
                print("5. Password comparison:")
                print(f"   - Stored password: '{stored_password}'")
                print(f"   - Input password: '{input_password}'")
                print(f"   - Length of stored password: {len(stored_password)}")
                print(f"   - Length of input password: {len(input_password)}")
                print(f"   - Are passwords equal? {stored_password == input_password}")
                
                if stored_password == input_password:
                    request.session['user_id'] = str(user['_id'])
                    request.session['username'] = user['username']
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': f"Welcome back {user['username']}",
                        'redirect': '/home/',
                        'user_id': str(user['_id'])
                    })
                else:
                    print("6. Password mismatch")
            else:
                print("3. No user found with this email")
            
            return JsonResponse({
                'status': 'error',
                'message': 'Wrong Email/Password'
            }, status=400)
                
        except Exception as e:
            print("Login error:", str(e))
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
            
    return render(request, 'intellishop/login.html')

def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Registration data:", data)  # Debug log
            
            # Check if user already exists
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
                password=data['password'],
                email=data['email'],
                status=data['status'],
                age=data['age'],
                location=data['location'],
                hobbies=data['hobbies']
            )
            print("Created user with ID:", user_id)  # Debug log
            
            return JsonResponse({
                'status': 'success', 
                'message': 'User registered successfully',
                'user_id': str(user_id)
            })
            
        except Exception as e:
            print("Registration error:", str(e))  # Debug log
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=400)
    
    return render(request, 'intellishop/register.html')

def dashboard(request):
    try:
        # Get all users from MongoDB without any sorting
        users = list(User.find())  # Convert cursor to list immediately
        
        # Process the users
        users_list = []
        for user in users:
            if user is not None:
                # Convert ObjectId to string and ensure all fields exist
                user_data = {
                    'username': user.get('username', ''),
                    'email': user.get('email', ''),
                    'password': user.get('password', ''),
                    'status': user.get('status', ''),
                    'age': user.get('age', ''),
                    'location': user.get('location', ''),
                    'hobbies': user.get('hobbies', []),
                    '_id': str(user.get('_id', ''))
                }
                users_list.append(user_data)
        
        return render(request, 'intellishop/dashboard.html', {'users': users_list})
        
    except Exception as e:
        # Handle any errors and return an error message
        return render(request, 'intellishop/dashboard.html', {
            'users': [],
            'error': f"Error loading users: {str(e)}"
        })

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

def coupon_detail(request, coupon_code):
        # You can store coupon details in a database or dictionary

    coupons = {
        'ILMAR12': {
            'code': 'ILMAR12',
            'discount': '7.48₪',
            'total': '56.11₪',
            'expiry': '16/04/2025'
        },
                # Add more coupons here

    }
    coupon = coupons.get(coupon_code)
    return render(request, 'intellishop/coupon_detail.html', {'coupon': coupon})