from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses import Status
from .models import Task


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='user1',
            password='testpass'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            password='testpass'
        )
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user1,
            status=self.status
        )

    def test_task_list_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_create_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(reverse('tasks:create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_detail_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('tasks:detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_update_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(
            reverse('tasks:update', args=[self.task.id]),
            {
                'name': 'Updated Task',
                'description': 'Updated Description',
                'status': self.status.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_by_author(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(
            reverse('tasks:delete', args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_by_non_author(self):
        self.client.login(username='user2', password='testpass')
        response = self.client.post(
            reverse('tasks:delete', args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
        # Check error message
        response = self.client.get(reverse('tasks:list'))
        self.assertContains(response, "Only task author can delete task")


class TaskAccessTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            author=self.user,
            status=self.status
        )

    def test_unauthenticated_access(self):
        urls = [
            reverse('tasks:list'),
            reverse('tasks:create'),
            reverse('tasks:detail', args=[self.task.id]),
            reverse('tasks:update', args=[self.task.id]),
            reverse('tasks:delete', args=[self.task.id]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='user1',
            password='testpass'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            password='testpass'
        )
        self.status1 = Status.objects.create(name='Status1')
        self.status2 = Status.objects.create(name='Status2')
        self.label1 = Label.objects.create(name='Label1')
        self.label2 = Label.objects.create(name='Label2')

        # Создаем задачи
        self.task1 = Task.objects.create(
            name='Task1',
            description='Desc1',
            author=self.user1,
            executor=self.user1,
            status=self.status1
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task2',
            description='Desc2',
            author=self.user2,
            executor=self.user2,
            status=self.status2
        )
        self.task2.labels.add(self.label2)

        self.client.login(username='user1', password='testpass')

    def test_filter_by_status(self):
        response = self.client.get(
            reverse('tasks:list'),
            {'status': self.status1.id}
        )
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_executor(self):
        response = self.client.get(
            reverse('tasks:list'),
            {'executor': self.user1.id}
        )
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_label(self):
        response = self.client.get(
            reverse('tasks:list'),
            {'labels': self.label1.id}
        )
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_self_tasks(self):
        task3 = Task.objects.create(
            name='Task3',
            description='Desc3',
            author=self.user1,
            status=self.status1
        )
        response = self.client.get(
            reverse('tasks:list'),
            {'self_tasks': 'true'}
        )

        self.assertContains(response, self.task1.name)
        self.assertContains(response, task3.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_combined(self):
        task3 = Task.objects.create(
            name='Task3',
            description='Desc3',
            author=self.user1,
            executor=self.user1,
            status=self.status1
        )
        task3.labels.add(self.label1)
        response = self.client.get(reverse('tasks:list'), {
            'status': self.status1.id,
            'executor': self.user1.id,
            'labels': self.label1.id,
            'self_tasks': 'true'
        })

        self.assertContains(response, task3.name)
        self.assertNotContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)