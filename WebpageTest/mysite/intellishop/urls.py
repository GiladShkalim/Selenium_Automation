# URL patterns that map URLs to view functions within the IntelliShop app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root route to index
    path('home/', views.index_home, name='index_home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('base/', views.template, name='template'),
    path('api/products/', views.product_list, name='product_list'),
    path('api/products/<str:product_id>/', views.product_detail, name='product_detail'),
    path('coupon_for_aliexpress/', views.aliexpress_coupons, name='aliexpress_coupons'),
] 