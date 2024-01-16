from django.db import models
from accounts.models import Vendor
# Create your models here.

class PurchaseOrder(models.Model):
    """ This model stores Purchase Orders"""
    STATUS_CHOICES = [
        ('pending', "PENDING"),
        ('completed', "COMPLETED"),
        ('canceled', "CANCELED"),
    ]
    po_number = models.CharField(max_length= 50)
    vendor = models.ForeignKey(Vendor , on_delete= models.CASCADE) 
    order_date = models.DateTimeField(auto_now_add = True) 
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length = 9, choices = STATUS_CHOICES) 
    quality_rating = models.FloatField(blank = True , null = True)
    issue_date = models.DateTimeField(auto_now_add = True)
    acknowledgment_date =  models.DateTimeField(null=True)
    delivered_ontime  = models.BooleanField(blank=True, null=True)

class HistoricalPerformance(models.Model):
    """ Vendor performance """
    vendor = models.ForeignKey(Vendor , on_delete= models.CASCADE) 
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0.0) 
    quality_rating_avg = models.FloatField(default=0.0) 
    average_response_time = models.FloatField(default=0.0) 
    fulfillment_rate =  models.FloatField(default=0.0)
