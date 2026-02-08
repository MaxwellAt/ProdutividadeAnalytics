from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.utils.dateparse import parse_datetime

from .models import Task, ActivityLog, Source
from .forms import TaskForm, UploadFileForm
from .services.analytics import AnalyticsService
from .services.task_service import TaskService


@login_required
def dashboard(request):
    context = {}
    try:
        context['kpis'] = AnalyticsService.get_kpis()
        context['chart_daily'] = AnalyticsService.get_productivity_chart()
        context['chart_pie'] = AnalyticsService.get_category_pie_chart()
        context['chart_source'] = AnalyticsService.get_source_pie_chart()
        context['chart_trend'] = AnalyticsService.get_weekly_trend()
    except Exception as e:
        print(f"Error generating analytics: {e}")
    
    return render(request, 'dashboard.html', context)


@login_required
def task_list(request):
    tasks = TaskService.get_all_tasks()
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Using basic save from form for now as it maps 1:1 to model, 
            # but we could extract data and use Service if logic was complex.
            # Ideally: TaskService.create_task(**form.cleaned_data)
            # Keeping form.save() for basic CRUD is standard Django, 
            # but to fully respect "Layer Separation", we do:
            TaskService.create_task(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                completed=form.cleaned_data['completed'],
                category_id=form.cleaned_data['category'].id if form.cleaned_data['category'] else None
            )
            return redirect('../')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


@login_required
def task_delete(request, id):
    TaskService.delete_task(id)
    return redirect('../')


@login_required
def task_update(request, id):
    task = TaskService.get_task_by_id(id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            # form.save() usually does the job, but delegating to service:
            TaskService.update_task(id, form.cleaned_data)
            return redirect('../')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = request.FILES['file']
                df = pd.read_csv(csv_file)
                
                # Basic validation
                required_cols = ['Start Time', 'End Time', 'Description']
                if not all(col in df.columns for col in required_cols):
                    messages.error(request, f"O arquivo CSV deve conter as colunas: {', '.join(required_cols)}")
                    return render(request, 'upload_csv.html', {'form': form})

                # Get or Create Source for CSV
                source, _ = Source.objects.get_or_create(name="CSV Import")

                count = 0
                for _, row in df.iterrows():
                    start = pd.to_datetime(row['Start Time'])
                    end = pd.to_datetime(row['End Time'])
                    
                    ActivityLog.objects.create(
                        start_time=start,
                        end_time=end,
                        description=row['Description'],
                        source=source
                    )
                    count += 1
                
                messages.success(request, f"{count} atividades importadas com sucesso! A classificação automática foi aplicada.")
                return redirect('dashboard')

            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {str(e)}")
    else:
        form = UploadFileForm()
    
    return render(request, 'upload_csv.html', {'form': form})
