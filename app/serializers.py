from app import models
from rest_framework import serializers
from authentication.api.serializers import UserSerializer


class InstanceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instance
        fields = ['id', 'id_string', 'name', 'icon', 'external_ico']
        extra_fields = []


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instance
        fields = ['id', 'id_string', 'name', 'icon', 'external_ico', 'rp', 'desc']

    def to_representation(self, instance):
        return super(InstanceSerializer, self).to_representation(instance)


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = '__all__'
        extra_fields = []

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ReportSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(ReportSerializer, self).to_representation(instance)
