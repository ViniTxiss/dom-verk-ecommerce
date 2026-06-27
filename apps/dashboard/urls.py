from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('pedidos/', views.dashboard_orders, name='orders'),
    path('pedidos/<int:order_id>/', views.dashboard_order_detail, name='order_detail'),
    path('produtos/', views.dashboard_products, name='products'),
]
