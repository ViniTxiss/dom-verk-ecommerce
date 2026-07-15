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


@require_POST
def apply_coupon(request):
    cart = Cart(request)
    if len(cart) == 0:
        return JsonResponse({'success': False, 'error': 'Seu carrinho está vazio.'}, status=400)

    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Dados inválidos.'}, status=400)

    if not code:
        return JsonResponse({'success': False, 'error': 'Informe o código do cupom.'}, status=400)

    from apps.orders.models import Coupon
    try:
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cupom inválido ou inexistente.'}, status=404)

    subtotal = cart.get_total_price()
    is_valid, msg = coupon.is_valid(subtotal=subtotal)
    if not is_valid:
        return JsonResponse({'success': False, 'error': msg}, status=400)

    discount = coupon.calculate_discount(subtotal)
    request.session['coupon_code'] = coupon.code
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'code': coupon.code,
        'discount_amount': float(discount),
        'discount_formatted': f"R$ {discount:.2f}".replace('.', ','),
        'subtotal_after_discount': float(subtotal - discount),
        'message': f"Cupom {coupon.code} aplicado com sucesso!",
    })


@require_POST
def remove_coupon(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        request.session.modified = True
    return JsonResponse({'success': True, 'message': 'Cupom removido.'})

