from rest_framework import serializers

from risks.models import RiskType, Risk


class JSONSerializerField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class RiskTypeSerializer(serializers.ModelSerializer):

    schema = JSONSerializerField()

    class Meta:
        model = RiskType
        fields = (
            'type_name',
            'schema',
            'is_active',
        )


class RiskSerializer(serializers.ModelSerializer):

    risk_type = RiskTypeSerializer(required=True)
    risk_data = JSONSerializerField()

    class Meta:
        model = Risk
        fields = (
            'risk_type',
            'risk_data',
        )