from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.products.urls', namespace='products')),
    path('carrinho/', include('apps.cart.urls', namespace='cart')),
    path('pedidos/', include('apps.orders.urls', namespace='orders')),
    path('conta/', include('apps.accounts.urls', namespace='accounts')),
    path('painel/', include('apps.dashboard.urls', namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
