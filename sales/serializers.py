from rest_framework import serializers
from .models import *
from django.db.models import Avg
from datetime import datetime
from django.utils import timezone
from rest_framework.serializers import ValidationError


class PurchaseOrderSerializer(serializers.ModelSerializer):
    issue_date = serializers.DateTimeField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = PurchaseOrder
        fields = ['items', "vendor", 'quantity','issue_date', 'id']

    def create(self, validated_data):
        return PurchaseOrder.objects.create(**validated_data)
    
class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['delivery_date']
    def validate_delivery_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('delivery date must be future date')
        return value

    def update(self, instance, validated_data):
        if 'delivery_date' in validated_data:
            instance.delivery_date = validated_data.pop('delivery_date')
            instance.acknowledgment_date = datetime.now()
            instance.extra_params = "acknowledged"
            instance.save()
            return instance
        raise ValidationError('data not allowed')
    
class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pk= kwargs.get('context').get('view').kwargs.get('pk')

        if PurchaseOrder.objects.get(id=pk).status =="completed":
            self.fields['status'].read_only = True

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            status_data = validated_data.pop('status')
            if status_data == 'completed':
                instance.status = status_data
                instance.extra_params = "completed"
                if instance.delivery_date <= timezone.now():
                    instance.delivered_ontime = True
                else:
                    instance.delivered_ontime = False
                instance.save()
                return instance
            else:
                return instance
        raise ValidationError('data not allowed')
        
class QualityRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['quality_rating']

    def validate_quality_rating(self,value):
        if value >5 or value <0:
            raise serializers.ValidationError('rate on the scale of 1-5')
        return value
    def update(self, instance, validated_data):
        if 'quality_rating' in validated_data:
            quality_rating = validated_data.pop('quality_rating')
            instance.quality_rating = quality_rating
            instance.extra_params = 'quality_rating'
            instance.save()
            return instance
        raise ValidationError('data not allowed')

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"