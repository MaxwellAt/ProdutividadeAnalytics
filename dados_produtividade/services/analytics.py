import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from ..models import ActivityLog, Task

class AnalyticsService:
    @staticmethod
    def get_kpis():
        # Tasks Stats
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(completed=True).count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Logs Stats (Total Hours)
        logs = ActivityLog.objects.all()
        total_hours = sum([l.duration_minutes for l in logs]) / 60.0 if logs else 0
        
        # Productive Hours
        prod_logs = logs.filter(category__is_productive=True)
        prod_hours = sum([l.duration_minutes for l in prod_logs]) / 60.0 if prod_logs else 0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": round(completion_rate, 1),
            "total_hours": round(total_hours, 1),
            "prod_hours": round(prod_hours, 1),
            "focus_score": int((prod_hours / total_hours * 100)) if total_hours > 0 else 0
        }

    @staticmethod
    def get_dataframe():
        logs = ActivityLog.objects.all().select_related('category', 'source').values(
            'start_time', 'duration_minutes', 'category__name', 'category__is_productive'
        )
        if not logs:
            return pd.DataFrame()
        
        df = pd.DataFrame(list(logs))
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['date'] = df['start_time'].dt.date
        return df

    @staticmethod
    def get_productivity_chart():
        df = AnalyticsService.get_dataframe()
        if df.empty:
            return None
        
        # Group by Date and Productivity
        daily = df.groupby(['date', 'category__is_productive'])['duration_minutes'].sum().reset_index()
        daily['Type'] = daily['category__is_productive'].apply(lambda x: 'Produtivo' if x else 'Distração')
        
        fig = px.bar(
            daily, 
            x='date', 
            y='duration_minutes', 
            color='Type',
            title='Produtividade Diária (Minutos)',
            color_discrete_map={'Produtivo': '#10b981', 'Distração': '#ef4444'},
            barmode='stack'
        )
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    @staticmethod
    def get_category_pie_chart():
        df = AnalyticsService.get_dataframe()
        if df.empty:
            return None
            
        total_by_cat = df.groupby('category__name')['duration_minutes'].sum().reset_index()
        
        fig = px.pie(
            total_by_cat, 
            values='duration_minutes', 
            names='category__name',
            title='Tempo por Categoria'
        )
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    @staticmethod
    def get_source_pie_chart():
        data = list(ActivityLog.objects.values('source__name', 'duration_minutes'))
        if not data: 
            return None
        df = pd.DataFrame(data)
        
        grp = df.groupby('source__name')['duration_minutes'].sum().reset_index()
        fig = px.pie(grp, values='duration_minutes', names='source__name', title='Fontes de Dados (Integração)', hole=0.4)
        return json.dumps(fig, cls=PlotlyJSONEncoder)
        
    @staticmethod
    def get_weekly_trend():
        df = AnalyticsService.get_dataframe()
        if df.empty: return None
        # Simple line chart for duration over time
        trend = df.groupby('date')['duration_minutes'].sum().reset_index()
        fig = px.line(trend, x='date', y='duration_minutes', title='Tendência Semanal de Foco', markers=True)
        return json.dumps(fig, cls=PlotlyJSONEncoder)
