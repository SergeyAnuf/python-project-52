from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User


class UserCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_user_create(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user_update', args=[self.user.id]), {
            'username': 'updateduser',
            'first_name': 'Updated',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())