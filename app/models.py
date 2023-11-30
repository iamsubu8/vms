from django.db import models
from django.utils import timezone

class Vendors(models.Model):
    name=models.CharField(max_length=100,blank=True)
    contact_details=models.TextField()
    address=models.TextField()
    vender_code=models.CharField(max_length=50,unique=True)
    on_time_delivery_rate=models.FloatField(null=True)
    quality_rating_avg=models.FloatField(null=True)
    average_response_time=models.FloatField(null=True) #in second
    fulfillment_rate=models.FloatField(null=True)

    def __str__(self) :
        return self.name
    class Meta:
        db_table="vendor"

class PO(models.Model):
    po_number=models.CharField(max_length=50,unique=True)
    vendor=models.ForeignKey("Vendors", on_delete=models.CASCADE)
    order_date=models.DateTimeField(default=timezone.now)
    delivery_date=models.DateTimeField()
    items=models.JSONField(null=True)
    quantity=models.IntegerField()
    status=models.CharField(max_length=50,default="pending")
    quality_rating=models.FloatField(null=True)
    issue_date=models.DateTimeField(null=True)
    acknowledgment_date=models.DateTimeField(null=True)

    class Meta:
        db_table="purchage_order"

class Historic_Performance(models.Model):
    vendor=models.ForeignKey("Vendors", on_delete=models.CASCADE)
    date=models.DateTimeField(null=True)
    on_time_delivery_rate=models.FloatField(null=True)
    quality_rating_avg=models.FloatField(null=True)
    average_response_time=models.FloatField(null=True)
    fulfillment_rate=models.FloatField(null=True)

    class Meta:
        db_table="historic_performance"
