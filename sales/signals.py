from django.dispatch import receiver
from django.db.models.signals import  post_save, pre_save
from .models import *
import uuid 
import random
from utility import *

from django.db.models import *

@receiver(pre_save, sender= PurchaseOrder)
def generate_po(sender, instance,**kwargs):
    if not instance.po_number:
        start_range = 0
        if PurchaseOrder.objects.all().exists():
            start_range = int (PurchaseOrder.objects.all().last().po_number)
        po = random.randint(start_range+1, start_range+1000)
        while PurchaseOrder.objects.filter(po_number = po).exists():
            po = random.randint(start_range+1, start_range+1000)
        instance.po_number = po
    return

@receiver(post_save, sender= PurchaseOrder)
def update_performance_data(sender, instance, created, **kwargs):
    if hasattr(instance, 'extra_params'):
        vendor_total_po = PurchaseOrder.objects.filter(vendor= instance.vendor.id)
        vendor = instance.vendor.id
        historical_obj = HistoricalPerformance.objects.filter(vendor= vendor)
        cur_historical_obj = historical_obj.filter(vendor__purchaseorder__id = instance.id).first()
        completed_po = vendor_total_po.filter(status='completed')
        if instance.extra_params == "completed":
            # fulfilment rate
            
            fulfillment_rate = calc_fulfilment_rate(0.0, completed_po , vendor_total_po)
            on_time_delivery_rate = calc_on_time_delivery(0.0, vendor_total_po)
    
            cur_historical_obj.fulfillment_rate = fulfillment_rate
            cur_historical_obj.on_time_delivery_rate = on_time_delivery_rate
            cur_historical_obj.save()
            return 
        elif instance.extra_params == "quality_rating":
            #quality rating average
            quality_rating_avg = completed_po.aggregate(quality_avg = Avg('quality_rating'))
            cur_historical_obj.quality_rating_avg = quality_rating_avg.get('quality_rating_avg',0.0)
            cur_historical_obj.save()
            return 
        elif instance.extra_params == "acknowledged":
            #average response time
            avg = vendor_total_po.annotate(difference = ExpressionWrapper(F('acknowledgment_date')-F('issue_date'),output_field=FloatField())).aggregate(avg_response_time=Avg('difference'))
            average_response_time = avg.get('avg_response_time')
            HistoricalPerformance.objects.create(vendor=instance.vendor, average_response_time = average_response_time)
            return 
    else:
        return