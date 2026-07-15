from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.orders.models import Coupon


class DashboardCouponsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = CustomUser.objects.create_user(
            username='admin_test',
            email='admin@example.com',
            password='password123',
            is_staff=True
        )
        self.normal_user = CustomUser.objects.create_user(
            username='normal_user',
            email='normal@example.com',
            password='password123',
            is_staff=False
        )
        self.coupon = Coupon.objects.create(
            code='WELCOME10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            active=True
        )

    def test_dashboard_coupons_requires_staff(self):
        # Usuário anônimo deve ser redirecionado para o login
        response = self.client.get(reverse('dashboard:coupons'))
        self.assertEqual(response.status_code, 302)

        # Usuário comum não-staff não deve acessar o dashboard
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('dashboard:coupons'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_coupons_list_access(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('dashboard:coupons'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'WELCOME10')

    def test_dashboard_coupon_create(self):
        self.client.force_login(self.staff_user)
        data = {
            'code': 'NIVER20',
            'discount_type': 'fixed',
            'discount_value': '20.00',
            'min_purchase_value': '100.00',
            'active': 'on',
        }
        response = self.client.post(reverse('dashboard:coupon_create'), data=data)
        self.assertEqual(response.status_code, 302)  # redireciona para a listagem
        self.assertTrue(Coupon.objects.filter(code='NIVER20').exists())
        coupon = Coupon.objects.get(code='NIVER20')
        self.assertEqual(coupon.discount_value, Decimal('20.00'))

    def test_dashboard_coupon_edit(self):
        self.client.force_login(self.staff_user)
        data = {
            'code': 'WELCOME10',
            'discount_type': 'percentage',
            'discount_value': '15.00',
            'min_purchase_value': '50.00',
            'active': 'on',
        }
        response = self.client.post(reverse('dashboard:coupon_edit', kwargs={'coupon_id': self.coupon.id}), data=data)
        self.assertEqual(response.status_code, 302)
        self.coupon.refresh_from_db()
        self.assertEqual(self.coupon.discount_value, Decimal('15.00'))

    def test_dashboard_coupon_toggle(self):
        self.client.force_login(self.staff_user)
        self.assertTrue(self.coupon.active)
        response = self.client.post(reverse('dashboard:coupon_toggle', kwargs={'coupon_id': self.coupon.id}))
        self.assertEqual(response.status_code, 302)
        self.coupon.refresh_from_db()
        self.assertFalse(self.coupon.active)
