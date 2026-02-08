from ..models import Task, Category

class TaskService:
    @staticmethod
    def get_all_tasks():
        """Returns all tasks ordered by creation date."""
        return Task.objects.all().order_by('-created_at')

    @staticmethod
    def get_task_by_id(task_id: int) -> Task:
        """Retrieves a single task or raises Task.DoesNotExist."""
        return Task.objects.get(id=task_id)

    @staticmethod
    def create_task(title: str, description: str = None, completed: bool = False, category_id: int = None) -> Task:
        """Encapsulates task creation logic."""
        category = None
        if category_id:
            category = Category.objects.get(id=category_id)
            
        task = Task.objects.create(
            title=title,
            description=description,
            completed=completed,
            category=category
        )
        return task

    @staticmethod
    def update_task(task_id: int, data: dict) -> Task:
        """
        Updates task fields dynamically based on provided dictionary.
        Handles 'category' specially if passed as ID.
        """
        task = Task.objects.get(id=task_id)
        
        for key, value in data.items():
            if key == 'category' and value is not None:
                # Assuming value is an instance or ID logic handled by caller
                # If Clean Architecture, we might expect ID here. 
                # For compatibility with Forms/DRF serializers which return instances, we check:
                task.category = value
            elif hasattr(task, key):
                setattr(task, key, value)
        
        task.save()
        return task

    @staticmethod
    def delete_task(task_id: int):
        """Hard deletes a task."""
        task = Task.objects.get(id=task_id)
        task.delete()
