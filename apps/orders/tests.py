from django.test import TestCase, Client
from django.urls import reverse
from apps.orders.models import Order

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
