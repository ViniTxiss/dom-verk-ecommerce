from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.products.urls', namespace='products')),
    path('carrinho/', include('apps.cart.urls', namespace='cart')),
    path('pedidos/', include('apps.orders.urls', namespace='orders')),
    path('conta/', include('apps.accounts.urls', namespace='accounts')),
    path('painel/', include('apps.dashboard.urls', namespace='dashboard')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
