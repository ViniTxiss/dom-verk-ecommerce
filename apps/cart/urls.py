from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('adicionar/', views.cart_add, name='add'),
    path('remover/', views.cart_remove, name='remove'),
    path('atualizar/', views.cart_update, name='update'),
    path('cupom/aplicar/', views.apply_coupon, name='apply_coupon'),
    path('cupom/remover/', views.remove_coupon, name='remove_coupon'),
]
