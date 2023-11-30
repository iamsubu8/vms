from rest_framework import serializers
from .models import *
from django.utils import timezone


class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ['name', 'contact_details', 'address', 'vender_code']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = "__all__"

class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ['name', 'contact_details', 'address']

class POCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PO
        fields = ['po_number', 'vendor', 'delivery_date', 'items', 'quantity', 'issue_date']
    
    def create(self, validated_data):
        validated_data['issue_date'] = timezone.now()
        return super().create(validated_data)

class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PO
        fields = "__all__"

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ['name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']