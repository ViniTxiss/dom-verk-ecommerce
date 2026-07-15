from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser


class AccountsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='user_test',
            email='test@example.com',
            password='Password123!',
            first_name='Carlos'
        )

    def test_login_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user_test',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carlos')

    def test_logout_post_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
