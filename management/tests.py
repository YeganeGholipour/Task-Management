from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Project, Task, Comment, StatusChoice
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
from .tasks import list_tasks_due_in_24_hours
from django.core import mail
from django.core.cache import cache
import time


class ProjectTest(TestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_create_project_right_data(self):
        data = {
            'name': 'Test Project',
            'description': 'This is a test project',
        }
        response = self.client.post(reverse('projects'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
    
    def test_create_project_wrong_data(self):
        data = {
            'name': 'Test Project',
        }
        response = self.client.post(reverse('projects'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Project.objects.count(), 0)
    
    def test_get_all_projects(self):
        Project.objects.create(name='Test Project', description='This is a test project')
        Project.objects.create(name='Test Project 2', description='This is a test project 2')
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_project_by_id(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        response = self.client.get(reverse('project', args=[project.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Project')
        self.assertEqual(response.data['description'], 'This is a test project')
        self.assertEqual(Project.objects.count(), 1)

    def test_update_project_right_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        data = {
            'name': 'Updated Project',
            'description': 'This is an updated project',
        }
        response = self.client.put(reverse('project', args=[project.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Project')
        self.assertEqual(response.data['description'], 'This is an updated project')
        self.assertEqual(Project.objects.count(), 1)
    
    def test_update_project_wrong_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        data = {
            'name': 'Updated Project',
        }
        response = self.client.put(reverse('project', args=[project.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Project.objects.count(), 1)

    def test_delete_project(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        response = self.client.delete(reverse('project', args=[project.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)



class TaskTest(TestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_create_task_right_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': StatusChoice.PENDING,
            'project': project.pk,
            'due_date': '2023-12-31T23:59:59Z'
        }
        response = self.client.post(reverse('tasks'), data)
        if response.status_code != status.HTTP_201_CREATED:
            print("****************************")
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_create_task_wrong_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'PENDING',
            'project': project.pk
            
        }
        response = self.client.post(reverse('tasks'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_get_all_tasks(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        Task.objects.create(title='Test Task', description='This is a test task', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        Task.objects.create(title='Test Task 2', description='This is a test task 2', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 
        self.assertEqual(Task.objects.count(), 2)
    
    def test_get_task_by_id(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        task = Task.objects.create(title='Test Task', description='This is a test task', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        response = self.client.get(reverse('task', args=[task.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')
        self.assertEqual(response.data['description'], 'This is a test task')
        self.assertEqual(Task.objects.count(), 1)
    
    def test_update_task_right_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        task = Task.objects.create(title='Test Task', description='This is a test task', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        data = {
            'title': 'Updated Task',
            'description': 'This is an updated task',
            'project': project.pk, 
            'status': StatusChoice.PENDING,
            'due_date': '2023-12-31T23:59:59Z'
        }
        response = self.client.put(reverse('task', args=[task.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')
        self.assertEqual(response.data['description'], 'This is an updated task')
        self.assertEqual(Task.objects.count(), 1)
    
    def test_update_task_wrong_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        task = Task.objects.create(title='Test Task', description='This is a test task', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        data = {
            'name': 'Updated Task',
            'project': project.pk
        }
        response = self.client.put(reverse('task', args=[task.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_delete_task(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        task = Task.objects.create(title='Test Task', description='This is a test task', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        response = self.client.delete(reverse('task', args=[task.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class CommentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_comment_right_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        task = Task.objects.create(title='Test Task', description='This is a test task', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        data = {
            'text': 'Test Comment',
            'author': 'Test Author',
        }
        url = reverse('comments', args=[task.pk])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_create_comment_wrong_data(self):
        project = Project.objects.create(name='Test Project', description='This is a test project')
        task = Task.objects.create(title='Test Task', description='This is a test task', project=project, status='PENDING', due_date='2023-12-31T23:59:59Z')
        data = {
            'text': 'Test Comment'
        }
        url = reverse('comments', args=[task.pk])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)



class CeleryTest(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        self.due = now + timedelta(hours=24)
        project = Project.objects.create(name='Test Project', description='This is a test project')
        self.task = Task.objects.create(title='Test Task', description='This is a test task', status='PENDING', due_date=self.due, project=project)
        self.recipient_list_emails = ["yeganegholiour@gmail.com"]
    def test_list_tasks_due_in_24_hours(self):
        mail.outbox = []

        list_tasks_due_in_24_hours.apply(
            args=[self.recipient_list_emails])

        sent_email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, self.recipient_list_emails)
        self.assertIn('Reminder for task:', sent_email.subject)
        self.assertIn(self.task.title, sent_email.body)
        self.assertIn('Due Date:', sent_email.body)

    def tearDown(self):
        self.task.delete()


class CacheTest(TestCase):
    def setUp(self):
        cache.clear()
    def test_get_and_set(self):
        cache.set('key', 'value')

        value = cache.get('key')
        self.assertEqual(value, 'value')

    def test_delete(self):
        cache.set('key', 'value')
        cache.delete('key')
        value = cache.get('key')
        self.assertIsNone(value)

    def test_cache_timeout(self):
        cache.set('key', 'value', timeout=1)
        time.sleep(2)
        value = cache.get('key')
        self.assertIsNone(value)