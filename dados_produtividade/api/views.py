from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from dados_produtividade.models import Task, ActivityLog, Category, Source, ClassificationRule
from .serializers import (
    TaskSerializer, ActivityLogSerializer, CategorySerializer,
    SourceSerializer, ClassificationRuleSerializer
)

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['completed', 'category']

class ActivityLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activity logs (Time Tracking).
    """
    queryset = ActivityLog.objects.all().order_by('-start_time')
    serializer_class = ActivityLogSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['description']
    filterset_fields = ['category', 'source', 'task']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class ClassificationRuleViewSet(viewsets.ModelViewSet):
    queryset = ClassificationRule.objects.all().order_by('-priority')
    serializer_class = ClassificationRuleSerializer
