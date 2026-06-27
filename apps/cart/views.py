import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.products.models import Product, ProductVariant
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def cart_add(request):
    cart = Cart(request)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)

    product = get_object_or_404(Product, id=product_id, is_active=True)

    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
        if variant.stock < quantity:
            return JsonResponse({'success': False, 'error': 'Estoque insuficiente'}, status=400)

    cart.add(product, variant_id, quantity)

    return JsonResponse({
        'success': True,
        'cart_count': cart.get_total_items(),
        'cart_total': str(cart.get_total_price()),
        'message': f'{product.name} adicionado ao carrinho!',
    })


@require_POST
def cart_remove(request):
    cart = Cart(request)
    try:
        data = json.loads(request.body)
        key = data.get('key')
    except json.JSONDecodeError:
        return JsonResponse({'success': False}, status=400)

    cart.remove(key)
    return JsonResponse({
        'success': True,
        'cart_count': cart.get_total_items(),
        'cart_total': str(cart.get_total_price()),
    })


@require_POST
def cart_update(request):
    cart = Cart(request)
    try:
        data = json.loads(request.body)
        key = data.get('key')
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False}, status=400)

    if key in cart.cart:
        if quantity <= 0:
            cart.remove(key)
        else:
            cart.cart[key]['quantity'] = quantity
            cart.save()

    return JsonResponse({
        'success': True,
        'cart_count': cart.get_total_items(),
        'cart_total': str(cart.get_total_price()),
    })
