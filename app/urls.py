from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'instances', views.InstanceViewSet)
router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path('imports', views.imports),
]
