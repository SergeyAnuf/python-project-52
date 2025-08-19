from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task, Status
from .models import Label


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.label = Label.objects.create(name='Test Label')

    def test_label_list_view(self):
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_label_create_view(self):
        response = self.client.post(reverse('labels:create'), {'name': 'New Label'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        response = self.client.post(
            reverse('labels:update', args=[self.label.id]),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete_view(self):
        response = self.client.post(
            reverse('labels:delete', args=[self.label.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_protected_delete(self):
        status = Status.objects.create(name='Test Status')
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user,
            status=status
        )
        task.labels.add(self.label)

        response = self.client.post(
            reverse('labels:delete', args=[self.label.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        response = self.client.get(reverse('labels:list'))
        self.assertContains(response, "Cannot delete label because it is in use")


class LabelAccessTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.label = Label.objects.create(name='Test Label')

    def test_unauthenticated_access(self):
        urls = [
            reverse('labels:list'),
            reverse('labels:create'),
            reverse('labels:update', args=[self.label.id]),
            reverse('labels:delete', args=[self.label.id]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")