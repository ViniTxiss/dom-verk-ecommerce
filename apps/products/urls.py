from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('loja/', views.product_list, name='list'),
    path('produto/<slug:slug>/', views.product_detail, name='detail'),
]
