from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacao/<int:order_id>/', views.order_confirmation, name='confirmation'),
    path('confirmacao/<int:order_id>/pagar/', views.simulate_payment, name='simulate_payment'),
    path('historico/', views.order_history, name='history'),
]
