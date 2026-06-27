from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('adicionar/', views.cart_add, name='add'),
    path('remover/', views.cart_remove, name='remove'),
    path('atualizar/', views.cart_update, name='update'),
]
