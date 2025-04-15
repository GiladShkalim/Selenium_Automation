# URL patterns that map URLs to view functions within the IntelliShop app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root route to index
    path('home/', views.index_home, name='index_home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('base/', views.template, name='template'),
] 