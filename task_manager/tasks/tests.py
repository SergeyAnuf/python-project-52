from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task, Status
from task_manager.labels.models import Label
from task_manager.users.models import User


class TaskTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass',
            first_name='User1',
            last_name='Test'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass',
            first_name='User2',
            last_name='Test'
        )
        self.status1 = Status.objects.create(name='Status1')
        self.status2 = Status.objects.create(name='Status2')
        self.label1 = Label.objects.create(name='Label1')
        self.label2 = Label.objects.create(name='Label2')

        # Создаем задачи
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user1,
            status=self.status1,
            executor=self.user2
        )
        self.task.labels.add(self.label1)

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
            'status': self.status1.id,
            'executor': self.user2.id,
            'labels': [self.label1.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_detail_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(
            reverse('tasks:detail', args=[self.task.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_update_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(
            reverse('tasks:update', args=[self.task.id]),
            {
                'name': 'Updated Task',
                'description': 'Updated Description',
                'status': self.status2.id,
                'executor': self.user1.id,
                'labels': [self.label2.id]
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view(self):
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
            self.assertRedirects(
                response, f"{reverse('login')}?next={url}"
            )

    def test_filter_by_status(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(
            reverse('tasks:list'),
            {'status': self.status1.id}
        )
        self.assertContains(response, self.task.name)

    def test_filter_by_executor(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(
            reverse('tasks:list'),
            {'executor': self.user2.id}
        )
        self.assertContains(response, self.task.name)

    def test_filter_by_label(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(
            reverse('tasks:list'),
            {'labels': self.label1.id}
        )
        self.assertContains(response, self.task.name)

    def test_filter_self_tasks(self):
        # Create a task for user2
        task2 = Task.objects.create(
            name='User2 Task',
            description='User2 Description',
            author=self.user2,
            status=self.status1,
            executor=self.user1
        )
        self.client.login(username='user2', password='testpass')
        response = self.client.get(
            reverse('tasks:list'),
            {'self_tasks': 'true'}
        )
        self.assertContains(response, task2.name)
        self.assertNotContains(response, self.task.name)

    def test_multiple_filters(self):
        task2 = Task.objects.create(
            name='Another Task',
            description='Another Description',
            author=self.user1,
            status=self.status1,
            executor=self.user1
        )
        task2.labels.add(self.label1)
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('tasks:list'), {
            'status': self.status1.id,
            'executor': self.user1.id,
            'labels': self.label1.id
        })
        self.assertContains(response, task2.name)