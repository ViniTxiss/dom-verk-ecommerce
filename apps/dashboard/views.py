from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.products.models import Product, Category
from apps.orders.models import Order


@staff_member_required
def dashboard_home(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    orders_today = Order.objects.filter(created_at__date=today)
    orders_week = Order.objects.filter(created_at__date__gte=week_ago)
    revenue_today = orders_today.aggregate(total=Sum('total'))['total'] or 0
    revenue_week = orders_week.aggregate(total=Sum('total'))['total'] or 0

    recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')[:10]
    total_products = Product.objects.filter(is_active=True).count()
    pending_orders = Order.objects.filter(status='pending').count()

    context = {
        'revenue_today': revenue_today,
        'revenue_week': revenue_week,
        'orders_today_count': orders_today.count(),
        'orders_week_count': orders_week.count(),
        'recent_orders': recent_orders,
        'total_products': total_products,
        'pending_orders': pending_orders,
    }
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def dashboard_orders(request):
    orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'dashboard/orders.html', {'orders': orders, 'status_filter': status_filter})


@staff_member_required
def dashboard_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return render(request, 'dashboard/order_detail.html', {'order': order})


@staff_member_required
def dashboard_products(request):
    products = Product.objects.select_related('category').prefetch_related('variants').order_by('-created_at')
    categories = Category.objects.filter(is_active=True)
    return render(request, 'dashboard/products.html', {'products': products, 'categories': categories})


@staff_member_required
def dashboard_product_create(request):
    categories = Category.objects.filter(is_active=True)
    if request.method == 'POST':
        try:
            product = Product(
                name=request.POST['name'],
                category_id=request.POST.get('category') or None,
                description=request.POST.get('description', ''),
                story=request.POST.get('story', ''),
                price=request.POST['price'],
                is_active=request.POST.get('is_active') == 'on',
                is_featured=request.POST.get('is_featured') == 'on',
                is_flash_deal=request.POST.get('is_flash_deal') == 'on',
            )
            promo = request.POST.get('price_promo', '').strip()
            if promo:
                product.price_promo = promo
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            if 'image_hover' in request.FILES:
                product.image_hover = request.FILES['image_hover']
            product.save()
            messages.success(request, f'Produto "{product.name}" criado com sucesso!')
            return redirect('dashboard:products')
        except Exception as e:
            messages.error(request, f'Erro ao criar produto: {e}')
    return render(request, 'dashboard/product_form.html', {'categories': categories, 'action': 'Criar'})


@staff_member_required
def dashboard_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.filter(is_active=True)
    if request.method == 'POST':
        try:
            product.name = request.POST['name']
            product.category_id = request.POST.get('category') or None
            product.description = request.POST.get('description', '')
            product.story = request.POST.get('story', '')
            product.price = request.POST['price']
            product.is_active = request.POST.get('is_active') == 'on'
            product.is_featured = request.POST.get('is_featured') == 'on'
            product.is_flash_deal = request.POST.get('is_flash_deal') == 'on'
            promo = request.POST.get('price_promo', '').strip()
            product.price_promo = promo if promo else None
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            if 'image_hover' in request.FILES:
                product.image_hover = request.FILES['image_hover']
            product.save()
            messages.success(request, f'Produto "{product.name}" atualizado!')
            return redirect('dashboard:products')
        except Exception as e:
            messages.error(request, f'Erro ao salvar: {e}')
    return render(request, 'dashboard/product_form.html', {
        'product': product,
        'categories': categories,
        'action': 'Editar',
    })


@staff_member_required
def dashboard_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Produto "{name}" excluído.')
    return redirect('dashboard:products')
