from django.shortcuts import render, redirect

from .models import Task, TaskForm


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


def task_delete(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('../')


def task_update(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('../')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})
