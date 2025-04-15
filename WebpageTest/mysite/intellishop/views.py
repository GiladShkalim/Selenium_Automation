# View functions that handle HTTP requests and return responses
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
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