# View functions that handle HTTP requests and return responses
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models.mongodb_models import Product
import json

def index(request):
    return render(request, 'intellishop/index.html')

def index_home(request):
    return render(request, 'intellishop/index_home_original.html')

def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'], password=data['password'])
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'redirect': '/dashboard/'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid credentials'
            }, status=400)
    return render(request, 'intellishop/login.html')

def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create new user
            user = User.objects.create(
                username=data['username'],
                password=data['password'],  # In production, hash the password
                email=data['email'],
                status=data['status'],
                age=data['age'],
                location=data['location'],
                hobbies=data['hobbies']
            )
            return JsonResponse({'status': 'success', 'message': 'User registered successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return render(request, 'intellishop/register.html')

def dashboard(request):
    # Get all users from the database
    users = User.objects.all()
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