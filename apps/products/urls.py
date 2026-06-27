from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('loja/', views.product_list, name='list'),
    path('produto/<slug:slug>/', views.product_detail, name='detail'),
    path('politica-de-privacidade/', views.privacy_policy, name='privacy_policy'),
    path('termos-de-uso/', views.terms_of_use, name='terms_of_use'),
    path('politica-de-troca/', views.exchanges, name='exchanges'),
    path('nossa-historia/', views.about, name='about'),
    path('guia-de-tamanhos/', views.size_guide, name='size_guide'),
]
