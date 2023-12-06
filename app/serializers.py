from rest_framework import serializers
from .models import *
from django.utils import timezone


class VendorCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, validators=[])
    class Meta:
        model = Vendors
        fields = ['contact_details', 'address', 'vender_code','name']
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("This filed required!")
        return value

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
        fields = "__all__"
    
    def create(self, validated_data):
        validated_data['issue_date'] = timezone.now()
        return super().create(validated_data)

class POSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    
    class Meta:
        model = PO
        fields = "__all__"

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ['name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

        