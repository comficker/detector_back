from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from base import pagination
from . import serializers
from app import models
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter
from rest_framework.decorators import api_view
from utils.detector import check_status
from django.utils import timezone
from django.db.models import Q


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ReportFilter(filters.FilterSet):
    created = DateFromToRangeFilter()

    class Meta:
        model = models.Report
        fields = [
            'instance__id_string',
            'created'
        ]


class InstanceViewSet(viewsets.ModelViewSet):
    models = models.Instance
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.InstanceSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["created", "today_report", "last_check"]
    search_fields = ['name', 'desc']

    lookup_field = 'id_string'

    def list(self, request, *args, **kwargs):
        q = Q()
        if request.GET.get("related"):
            q = q & Q(labels__instances__id_string=request.GET.get("related"))
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(q)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ReportViewSet(viewsets.ModelViewSet):
    models = models.Report
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.ReportSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = ReportFilter
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        request.data["ip"] = get_client_ip(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user if request.user.is_authenticated else None)
        headers = self.get_success_headers(serializer.data)
        instance = models.Report.objects.get(pk=serializer.data["id"]).instance
        now = timezone.now()
        if not (
                instance.last_check.year == now.year and
                instance.last_check.month == now.month and
                instance.last_check.day == now.year):
            instance.today_report = 0
        instance.today_report = instance.today_report + 1
        now = timezone.now()
        instance.last_check = now
        if request.user.is_authenticated and len(instance.reports.filter(created__gt=timezone.now())) < 100:
            instance.generate_reports(not check_status(instance.callback))
        instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def imports(request):
    if request.user.is_authenticated and request.user.id == 1:
        for item in request.data["ds"]:
            instance, created = models.Instance.objects.get_or_create(
                id_string=item.get("id_string"),
                defaults={
                    "name": item["name"],
                    "callback": item["callback"],
                    "desc": item["desc"],
                    "external_ico": item["external_ico"],
                }
            )
            if created:
                instance.generate_reports(item.get("is_down", False))
                if item.get("str_labels"):
                    for label_raw in item.get("labels"):
                        label, _ = models.Label.objects.get_or_create(
                            name=label_raw
                        )
                        instance.labels.add(label)
    return Response(status=status.HTTP_201_CREATED)
