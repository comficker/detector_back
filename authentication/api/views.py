from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from base import pagination
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    models = User
    queryset = User.objects.order_by('-id')
    serializer_class = serializers.UserSerializer
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
