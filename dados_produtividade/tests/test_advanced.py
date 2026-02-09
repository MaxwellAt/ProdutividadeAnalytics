import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from dados_produtividade.models import Task, ActivityLog
from dados_produtividade.services.task_service import TaskService

@pytest.mark.django_db
class TestTaskServiceLogic:
    def test_service_create(self):
        """Test Service Create Logic independent of View"""
        task = TaskService.create_task(title="Service Task", completed=True)
        assert task.id is not None
        assert task.title == "Service Task"
        # Business logic: completed tasks get a timestamp
        assert task.completed_at is not None 

    def test_service_update(self):
        """Test Service Update Logic"""
        task = TaskService.create_task(title="Old Title")
        updated = TaskService.update_task(task.id, {'title': 'New Title'})
        assert updated.title == 'New Title'

@pytest.mark.django_db
class TestAnalyticsAPI:
    @pytest.fixture
    def api_client(self):
        user = User.objects.create_user(username='analytics_user', password='password')
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_kpis_endpoint(self, api_client):
        """Ensure /api/v1/analytics/ returns JSON stats"""
        # Create some data
        TaskService.create_task(title="T1", completed=True)
        TaskService.create_task(title="T2", completed=False)
        
        url = '/api/v1/analytics/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Validating specific JSON structure
        assert 'total_tasks' in data
        assert data['total_tasks'] == 2
        assert data['completed_tasks'] == 1
        assert data['completion_rate'] == 50.0

    def test_auth_protection(self):
        """Analytics should be protected"""
        client = APIClient() # No auth
        response = client.get('/api/v1/analytics/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
