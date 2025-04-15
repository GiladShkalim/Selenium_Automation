# View functions that handle HTTP requests and return responses
from django.shortcuts import render

def index(request):
    return render(request, 'intellishop/index.html')

def index_home(request):
    return render(request, 'intellishop/index_home_original.html')

def login_view(request):
    return render(request, 'intellishop/login.html')

def register(request):
    return render(request, 'intellishop/register.html') 

def template(request):
    return render(request, 'intellishop/Site_template.html') 