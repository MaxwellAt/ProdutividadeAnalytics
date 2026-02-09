from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..services.analytics import AnalyticsService

class AnalyticsViewSet(viewsets.ViewSet):
    """
    API endpoint that returns calculated productivity metrics.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Return global KPIs.
        """
        try:
            kpis = AnalyticsService.get_kpis()
            return Response(kpis)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def weekly_trend(self, request):
        """
        Return Weekly Trend Chart Data (Plotly JSON).
        """
        data = AnalyticsService.get_weekly_trend()
        return Response(data)

    @action(detail=False, methods=['get'])
    def productivity_chart(self, request):
        """
        Return Daily Productivity Chart Data (Plotly JSON).
        """
        data = AnalyticsService.get_productivity_chart()
        return Response(data)
