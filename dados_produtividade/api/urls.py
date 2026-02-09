from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TaskViewSet, ActivityLogViewSet, CategoryViewSet,
    SourceViewSet, ClassificationRuleViewSet
)
from .analytics_view import AnalyticsViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'activities', ActivityLogViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sources', SourceViewSet)
router.register(r'rules', ClassificationRuleViewSet)

# Analytics is a ViewSet but doesn't map to a model directly locally, 
# so we register it with a basename
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]
