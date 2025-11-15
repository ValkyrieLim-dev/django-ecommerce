from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    # --- Home page redirects to login ---
    path('', views.home, name='home'),

    # --- Product pages ---
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # --- Cart pages ---
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),

    # --- Checkout pages ---
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<int:order_id>/', views.checkout_success, name='checkout_success'),

    # --- Authentication ---
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='store:login'), name='logout'),
    path('register/', views.register, name='register'),
]
