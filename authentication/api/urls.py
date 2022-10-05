from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()

urlpatterns = [
    path(r'', include(router.urls)),
]
