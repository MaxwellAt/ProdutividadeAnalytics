import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from dados_produtividade.models import Task, User

@pytest.mark.django_db
class TestTaskAPI:
    @pytest.fixture
    def api_client(self):
        user = User.objects.create_user(username='apiuser', password='password')
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_list_tasks(self, api_client):
        Task.objects.create(title="API Task 1")
        Task.objects.create(title="API Task 2")
        
        url = reverse('task-list') # DRF default router name
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_create_task(self, api_client):
        url = reverse('task-list')
        data = {'title': 'New API Task', 'description': 'Testing Create'}
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1
        assert Task.objects.get().title == 'New API Task'

    def test_unauthorized_access(self):
        client = APIClient()
        url = reverse('task-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
