from rest_framework import serializers
from dados_produtividade.models import Task, ActivityLog, Category, Source, ClassificationRule

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_productive', 'color']

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name']

class ClassificationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassificationRule
        fields = ['id', 'keyword', 'category', 'priority']

class TaskSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'description', 'created_at', 'completed_at', 'category', 'category_detail']
        read_only_fields = ['created_at', 'completed_at']

class ActivityLogSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    source_detail = SourceSerializer(source='source', read_only=True)
    task_detail = TaskSerializer(source='task', read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            'id', 'start_time', 'end_time', 'duration_minutes', 
            'description', 'category', 'source', 'task',
            'category_detail', 'source_detail', 'task_detail'
        ]
        read_only_fields = ['duration_minutes']
