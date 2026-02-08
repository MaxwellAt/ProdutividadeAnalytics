from django.contrib import admin
from .models import Task, Category, Source, ActivityLog

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completed', 'created_at')
    list_filter = ('completed', 'category')
    search_fields = ('title',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_productive', 'color')

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('description', 'duration_minutes', 'start_time', 'category', 'source')
    list_filter = ('category', 'source', 'start_time')
    date_hierarchy = 'start_time'

