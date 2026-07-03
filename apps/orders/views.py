from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cart.cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('cart:detail')

    # Pré-preencher com dados do usuário logado
    initial = {}
    if request.user.is_authenticated:
        u = request.user
        initial = {
            'buyer_name': u.get_full_name() or u.username,
            'buyer_email': u.email,
            'buyer_phone': u.phone,
            'buyer_cpf': u.cpf,
            'address_zip': u.address_zip,
            'address_street': u.address_street,
            'address_number': u.address_number,
            'address_complement': u.address_complement,
            'address_neighborhood': u.address_neighborhood,
            'address_city': u.address_city,
            'address_state': u.address_state,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.subtotal = cart.get_total_price()

            # Frete grátis acima de R$ 199
            order.shipping = 0 if order.subtotal >= 199 else 19.90

            # Desconto PIX (10%)
            if order.payment_method == 'pix':
                order.discount = order.subtotal * 10 / 100
            else:
                order.discount = 0

            order.total = order.subtotal + order.shipping - order.discount
            order.save()

            # Criar itens do pedido
            for item in cart:
                if item.get('variant') and item.get('product'):
                    OrderItem.objects.create(
                        order=order,
                        variant=item['variant'],
                        product_name=item['product'].name,
                        product_color=item['variant'].color,
                        product_size=item['variant'].size,
                        price=item['price'],
                        quantity=item['quantity'],
                    )

            cart.clear()
            messages.success(request, f'Pedido #{order.order_number} realizado com sucesso!')
            return redirect('orders:confirmation', order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
        'subtotal': cart.get_total_price(),
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/confirmation.html', {'order': order})


def simulate_payment(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        if order.status == 'pending':
            order.status = 'paid'
            order.save()
            messages.success(request, 'Simulação de pagamento aprovada! Seu pedido foi confirmado.')
        else:
            messages.warning(request, 'Este pedido já não está pendente de pagamento.')
    return redirect('orders:confirmation', order_id=order_id)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/history.html', {'orders': orders})
