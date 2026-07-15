from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.orders.models import Order, Coupon
from apps.products.models import Category, Product, ProductVariant

class OrderConfirmationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            buyer_name='João Silva',
            buyer_email='joao@example.com',
            buyer_phone='11999999999',
            buyer_cpf='12345678909',
            address_street='Rua Teste',
            address_number='123',
            address_neighborhood='Centro',
            address_city='São Paulo',
            address_state='SP',
            address_zip='01001000',
            subtotal=100.00,
            shipping=0.00,
            total=100.00,
            payment_method='pix'
        )
        # Registra o pedido na sessão (simula o fluxo real do checkout — _can_access_order)
        session = self.client.session
        session['confirmed_orders'] = [self.order.id]
        session.save()

    def test_order_confirmation_page(self):
        response = self.client.get(reverse('orders:confirmation', kwargs={'order_id': self.order.id}))
        self.assertEqual(response.status_code, 200)

    def test_simulate_payment_post_updates_status(self):
        response = self.client.post(reverse('orders:simulate_payment', kwargs={'order_id': self.order.id}))
        self.assertEqual(response.status_code, 302)  # redirects back
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')

    def test_simulate_payment_post_ignores_non_pending(self):
        self.order.status = 'delivered'
        self.order.save()
        response = self.client.post(reverse('orders:simulate_payment', kwargs={'order_id': self.order.id}))
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'delivered')  # status unchanged

    def test_order_confirmation_blocked_for_strangers(self):
        """Garante que um cliente sem sessão não acessa pedido alheio."""
        other_client = Client()  # sessão limpa, sem confirmed_orders
        response = other_client.get(reverse('orders:confirmation', kwargs={'order_id': self.order.id}))
        self.assertEqual(response.status_code, 302)  # redireciona para home

    def test_simulate_payment_blocked_for_strangers(self):
        """Garante que um cliente sem sessão não consegue simular pagamento alheio."""
        other_client = Client()
        response = other_client.post(reverse('orders:simulate_payment', kwargs={'order_id': self.order.id}))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')  # status não alterado


class CheckoutPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Camisetas', slug='camisetas')
        self.product = Product.objects.create(
            name='Camiseta Barata',
            slug='camiseta-barata',
            category=self.category,
            price=100.00,
            is_active=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color='preto',
            size='M',
            stock=10
        )
        # Adicionar item ao carrinho (subtotal 100 < 199, frete 19.90 deve ser calculado em Decimal)
        self.client.post(
            reverse('cart:add'),
            content_type='application/json',
            data={'product_id': self.product.id, 'variant_id': self.variant.id, 'quantity': 1}
        )

    def test_checkout_post_with_shipping_fee_decimal_success(self):
        """Testa checkout com frete pago (< 199) garantindo que soma de Decimal + frete não gera 500 TypeError."""
        data = {
            'buyer_name': 'Carlos Silva',
            'buyer_email': 'carlos@example.com',
            'buyer_phone': '11988887777',
            'buyer_cpf': '123.456.789-00',
            'address_zip': '01001-000',
            'address_street': 'Rua Flores',
            'address_number': '456',
            'address_complement': 'Apto 12',
            'address_neighborhood': 'Jardins',
            'address_city': 'São Paulo',
            'address_state': 'SP',
            'payment_method': 'pix',
            'notes': 'Entregar a tarde'
        }
        response = self.client.post(reverse('orders:checkout'), data=data)
        self.assertEqual(response.status_code, 302)
        order = Order.objects.latest('id')
        self.assertEqual(order.subtotal, Decimal('100.00'))
        self.assertEqual(order.shipping, Decimal('19.90'))
        # Desconto PIX 10% sobre 100 = 10.00
        self.assertEqual(order.discount, Decimal('10.00'))
        # Total = 100 + 19.90 - 10 = 109.90
        self.assertEqual(order.total, Decimal('109.90'))


class CouponModelTest(TestCase):
    def test_coupon_upper_case(self):
        coupon = Coupon.objects.create(code='promo10', discount_type='percentage', discount_value=10)
        self.assertEqual(coupon.code, 'PROMO10')

    def test_coupon_validity_active(self):
        coupon = Coupon.objects.create(code='TEST10', discount_type='percentage', discount_value=10)
        is_valid, msg = coupon.is_valid(subtotal=50)
        self.assertTrue(is_valid)

    def test_coupon_validity_inactive(self):
        coupon = Coupon.objects.create(code='INACTIVE', discount_type='percentage', discount_value=10, active=False)
        is_valid, msg = coupon.is_valid(subtotal=50)
        self.assertFalse(is_valid)

    def test_coupon_min_purchase_value(self):
        coupon = Coupon.objects.create(code='MIN100', discount_type='fixed', discount_value=20, min_purchase_value=100)
        is_valid_low, _ = coupon.is_valid(subtotal=50)
        self.assertFalse(is_valid_low)
        is_valid_high, _ = coupon.is_valid(subtotal=150)
        self.assertTrue(is_valid_high)

    def test_coupon_calculate_discount_percentage(self):
        coupon = Coupon.objects.create(code='PERC10', discount_type='percentage', discount_value=10)
        discount = coupon.calculate_discount(Decimal('200.00'))
        self.assertEqual(discount, Decimal('20.00'))

    def test_coupon_calculate_discount_fixed(self):
        coupon = Coupon.objects.create(code='FIXED15', discount_type='fixed', discount_value=15)
        discount = coupon.calculate_discount(Decimal('50.00'))
        self.assertEqual(discount, Decimal('15.00'))


class CouponViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.coupon = Coupon.objects.create(code='DOM10', discount_type='percentage', discount_value=10)
        self.category = Category.objects.create(name='Camisetas', slug='camisetas')
        self.product = Product.objects.create(
            name='Camiseta Teste',
            slug='camiseta-teste',
            category=self.category,
            price=100.00,
            is_active=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color='preto',
            size='M',
            stock=10
        )

    def test_apply_coupon_empty_cart_returns_400(self):
        response = self.client.post(
            reverse('cart:apply_coupon'),
            content_type='application/json',
            data={'code': 'DOM10'}
        )
        self.assertEqual(response.status_code, 400)

    def test_apply_coupon_invalid_code_returns_404(self):
        self.client.post(
            reverse('cart:add'),
            content_type='application/json',
            data={'product_id': self.product.id, 'variant_id': self.variant.id, 'quantity': 1}
        )
        response = self.client.post(
            reverse('cart:apply_coupon'),
            content_type='application/json',
            data={'code': 'INVALIDCODE'}
        )
        self.assertEqual(response.status_code, 404)

    def test_apply_and_remove_coupon_success(self):
        self.client.post(
            reverse('cart:add'),
            content_type='application/json',
            data={'product_id': self.product.id, 'variant_id': self.variant.id, 'quantity': 1}
        )
        response = self.client.post(
            reverse('cart:apply_coupon'),
            content_type='application/json',
            data={'code': 'DOM10'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['code'], 'DOM10')
        self.assertEqual(data['discount_amount'], 10.0)

        rem_response = self.client.post(reverse('cart:remove_coupon'))
        self.assertEqual(rem_response.status_code, 200)

