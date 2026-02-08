from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TaskViewSet, ActivityLogViewSet, CategoryViewSet,
    SourceViewSet, ClassificationRuleViewSet
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'activities', ActivityLogViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sources', SourceViewSet)
router.register(r'rules', ClassificationRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
