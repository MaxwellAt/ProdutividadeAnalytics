import pytest
from datetime import timedelta
from django.utils import timezone
from dados_produtividade.models import ActivityLog, Category, Source
from dados_produtividade.services.analytics import AnalyticsService

@pytest.mark.django_db
class TestAnalyticsService:
    @pytest.fixture
    def sample_data(self):
        cat_work = Category.objects.create(name="Work", is_productive=True)
        cat_leisure = Category.objects.create(name="Leisure", is_productive=False)
        src_ws = Source.objects.create(name="Workstation")
        
        # Today
        now = timezone.now()
        
        # 2 Hours Work
        ActivityLog.objects.create(
            start_time=now - timedelta(hours=2),
            end_time=now,
            description="Deep Work",
            category=cat_work,
            source=src_ws
        )
        
        # 1 Hour Leisure
        ActivityLog.objects.create(
            start_time=now - timedelta(hours=4),
            end_time=now - timedelta(hours=3),
            description="Gaming",
            category=cat_leisure,
            source=src_ws
        )
        return cat_work, cat_leisure

    def test_get_kpis(self, sample_data):
        kpis = AnalyticsService.get_kpis()
        
        # Checking values directly as get_kpis returns a flat dict of values
        assert isinstance(kpis['total_hours'], float) or isinstance(kpis['total_hours'], int)
        
        # We created 3 hours of logs in sample_data
        # 2h Work + 1h Leisure = 3.0 total
        assert kpis['total_hours'] == 3.0
        
        # Productive hours (Work) = 2.0
        assert kpis['prod_hours'] == 2.0
        
        # Focus score = 2/3 = ~66%
        assert kpis['focus_score'] == 66

    def test_charts_generation(self, sample_data):
        """Ensure Plotly JSONs are generated without error"""
        pie = AnalyticsService.get_category_pie_chart()
        assert isinstance(pie, str)
        assert "Work" in pie
        assert "Leisure" in pie

        daily = AnalyticsService.get_productivity_chart()
        assert isinstance(daily, str) # Returns JSON string
        
    def test_empty_database_resilience(self):
        """Service should not crash if DB is empty"""
        kpis = AnalyticsService.get_kpis()
        assert kpis['total_hours'] == 0
        
        chart = AnalyticsService.get_productivity_chart()
        # Chart returns None or empty JSON string when empty, checking truthiness or specific return
        if chart:
             assert isinstance(chart, str)
        else:
             assert chart is None
