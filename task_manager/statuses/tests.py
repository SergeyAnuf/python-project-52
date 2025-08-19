from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.status = Status.objects.create(name='Test Status')
        self.client.login(username='testuser', password='testpass')

    def test_status_list_view(self):
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_status_create_view(self):
        response = self.client.post(reverse('statuses:create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        response = self.client.post(
            reverse('statuses:update', args=[self.status.id]),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        response = self.client.post(
            reverse('statuses:delete', args=[self.status.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_protected_delete(self):
        pass

    def test_access_control(self):
        self.client.logout()

        urls = [
            reverse('statuses:list'),
            reverse('statuses:create'),
            reverse('statuses:update', args=[self.status.id]),
            reverse('statuses:delete', args=[self.status.id]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")