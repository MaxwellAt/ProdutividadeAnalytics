from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_productive = models.BooleanField(default=True)
    color = models.CharField(max_length=7, default="#FFFFFF") # Hex code

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=100) # e.g., WakaTime, Manual
    api_key = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class ClassificationRule(models.Model):
    """
    Rules to auto-classify incoming activity logs based on keywords.
    Ex: keyword='netflix' -> category='Entertainment'
        keyword='vscode' -> category='Coding'
    """
    keyword = models.CharField(max_length=100, help_text="Keyword to match in activity description (case-insensitive)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0, help_text="Higher priority rules run first")

    def __str__(self):
        return f"Contain '{self.keyword}' -> {self.category.name}"

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.completed and self.completed_at is None:
            self.completed_at = timezone.now()
        elif not self.completed and self.completed_at is not None:
            self.completed_at = None
        super().save(*args, **kwargs)

class ActivityLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.FloatField(editable=False)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # 1. Calculate Duration
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration_minutes = delta.total_seconds() / 60.0
        else:
            self.duration_minutes = 0.0

        # 2. Auto-Classification Engine
        # Only run if category is missing and we have a description
        if not self.category and self.description:
            try:
                # Find matching rules ordered by priority
                rules = ClassificationRule.objects.all().order_by('-priority')
                for rule in rules:
                    if rule.keyword.lower() in self.description.lower():
                        self.category = rule.category
                        break
            except Exception:
                pass # Fail silently, leave category null

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.description} ({self.duration_minutes:.1f} min)"

