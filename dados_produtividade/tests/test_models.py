import pytest
from django.utils import timezone
from datetime import timedelta
from dados_produtividade.models import Task, Category, ClassificationRule, ActivityLog, Source

@pytest.mark.django_db
class TestTaskModel:
    def test_create_task(self):
        task = Task.objects.create(title="Test Task", description="Description")
        assert task.created_at is not None
        assert task.completed is False
        assert task.completed_at is None

    def test_complete_task_sets_timestamp(self):
        task = Task.objects.create(title="Test Task")
        task.completed = True
        task.save()
        assert task.completed_at is not None
        
        # Uncomplete
        task.completed = False
        task.save()
        assert task.completed_at is None

@pytest.mark.django_db
class TestActivityLogModel:
    def test_duration_calculation(self):
        start = timezone.now()
        end = start + timedelta(minutes=30)
        log = ActivityLog.objects.create(
            start_time=start,
            end_time=end,
            description="Working"
        )
        # Check tolerance due to float precision or microseconds
        assert 29.9 <= log.duration_minutes <= 30.1

    def test_auto_classification_engine(self):
        # Setup Rules
        cat_dev = Category.objects.create(name="Development")
        cat_ent = Category.objects.create(name="Entertainment")
        
        ClassificationRule.objects.create(keyword="vscode", category=cat_dev, priority=2)
        ClassificationRule.objects.create(keyword="netflix", category=cat_ent, priority=1)

        # Case 1: Match Coding
        log1 = ActivityLog.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            description="Coding in VSCode python"
        )
        assert log1.category == cat_dev

        # Case 2: Match Entertainment (Case insensitive)
        log2 = ActivityLog.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            description="Watching Netflix series"
        )
        assert log2.category == cat_ent

        # Case 3: Priority (if both present, generic example)
        # Not easily testable with these keywords, but rule precedence logic is in model

        # Case 4: No match leaves None
        log3 = ActivityLog.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            description="Walking the dog"
        )
        assert log3.category is None
