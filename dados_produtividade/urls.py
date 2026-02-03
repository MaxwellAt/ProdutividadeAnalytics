from django.urls import path

from . import views

urlpatterns = [
    path('', views.task_list, name='taskList'),
    path('tasks/', views.task_create, name='tasksAdmin'),
    path('tasks_delete/<int:id>', views.task_delete, name='deleteTasks'),
    path('tasks_update/<int:id>', views.task_update, name='updateTasks'),
]
