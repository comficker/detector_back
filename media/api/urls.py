from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'medias', views.MediaViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
