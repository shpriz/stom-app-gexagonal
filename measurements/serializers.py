from rest_framework import serializers
from .models import Measurement, MeasurementValue
from indicators.models import Indicator
from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'full_name', 'date_of_birth']


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ['id', 'name', 'min_value', 'max_value', 'unit', 'green_threshold', 'yellow_threshold']


class MeasurementValueSerializer(serializers.ModelSerializer):
    indicator = IndicatorSerializer(read_only=True)
    color_zone = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = MeasurementValue
        fields = ['indicator', 'value', 'color_zone', 'percentage']
    
    def get_color_zone(self, obj):
        return obj.get_color_zone()
    
    def get_percentage(self, obj):
        return obj.get_percentage()


class MeasurementSerializer(serializers.ModelSerializer):
    values = MeasurementValueSerializer(many=True, read_only=True)
    patient = PatientSerializer(read_only=True)
    
    class Meta:
        model = Measurement
        fields = ['id', 'patient', 'measurement_date', 'show_in_chart', 'notes', 'values']


class RadarChartDataSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    patient_name = serializers.CharField()
    measurements = serializers.ListField(
        child=serializers.DictField()
    )
    indicators = serializers.ListField(
        child=IndicatorSerializer()
    )