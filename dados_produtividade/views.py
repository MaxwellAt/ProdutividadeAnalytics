from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from django.utils.dateparse import parse_datetime

from .models import Task, ActivityLog
from .forms import TaskForm, UploadFileForm
from .services.analytics import AnalyticsService


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

                count = 0
                for _, row in df.iterrows():
                    start = pd.to_datetime(row['Start Time'])
                    end = pd.to_datetime(row['End Time'])
                    
                    ActivityLog.objects.create(
                        start_time=start,
                        end_time=end,
                        description=row['Description']
                    )
                    count += 1
                
                messages.success(request, f"{count} atividades importadas com sucesso! A classificação automática foi aplicada.")
                return redirect('dashboard')

            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {str(e)}")
    else:
        form = UploadFileForm()
    
    return render(request, 'upload_csv.html', {'form': form})
