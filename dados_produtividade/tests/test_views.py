import pytest
from django.urls import reverse
from dados_produtividade.models import Task
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestViews:
    @pytest.fixture
    def auto_login_user(self, client):
        user = User.objects.create_user(username='testuser', password='password')
        client.login(username='testuser', password='password')
        return client, user

    def test_dashboard_login_required(self, client):
        """Unauthenticated users should be redirected"""
        url = reverse('dashboard')
        response = client.get(url)
        assert response.status_code == 302
        assert '/admin/login/' in response.url

    def test_dashboard_access_authorized(self, auto_login_user):
        """Authenticated users can see dashboard"""
        client, user = auto_login_user
        url = reverse('dashboard')
        response = client.get(url)
        assert response.status_code == 200
        # Check if context contains our analytic keys
        assert 'kpis' in response.context
        assert 'chart_daily' in response.context

    def test_task_crud(self, auto_login_user):
        client, user = auto_login_user
        
        # Create
        create_url = reverse('tasksAdmin')
        client.post(create_url, {
            'title': 'New Pytest Task', 
            'description': 'Created via test',
            'completed': False
        })
        assert Task.objects.count() == 1
        
        # List
        list_url = reverse('taskList')
        response = client.get(list_url)
        assert 'New Pytest Task' in str(response.content)

    def test_upload_csv_view(self, auto_login_user):
        client, user = auto_login_user
        url = reverse('upload_csv')
        
        # GET form
        response = client.get(url)
        assert response.status_code == 200
        
        # POST Invalid CSV (Missing columns)
        from django.core.files.uploadedfile import SimpleUploadedFile
        csv_content = b"header1,header2\nval1,val2"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        response = client.post(url, {'file': csv_file})
        messages = list(response.context['messages'])
        assert len(messages) > 0
        assert "O arquivo CSV deve conter as colunas" in str(messages[0])
