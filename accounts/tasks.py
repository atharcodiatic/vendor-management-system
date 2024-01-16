from celery import shared_task 
from django.dispatch import receiver
from django.db.models.signals import  post_save
from smtplib import SMTPException
from django.conf import settings
from sales.models import *
from .models import *
from vendorManagementSystem.celery import app
from django.db.models import *
from django.db.models.functions import Coalesce
from django_celery_beat.models import PeriodicTask, PeriodicTasks

@shared_task
def update_vendorprofile():
    print("TASK CELERY") 
    vendor_data  = Vendor.objects.annotate(avg_resp_time=Coalesce(Avg('historicalperformance__average_response_time'), Value(0), output_field=FloatField()), 
                             on_time_per= ExpressionWrapper(Coalesce(Avg('historicalperformance__on_time_delivery_rate'), Value(0)) * 100, output_field=FloatField()),     
    fulfillment_per=ExpressionWrapper(Coalesce(Avg('historicalperformance__fulfillment_rate'), Value(0)) * 100, output_field=FloatField()),
    quality_rat_avg=Coalesce(Avg('historicalperformance__quality_rating_avg'), Value(0), output_field=FloatField()), 
                             )
    for vendor in vendor_data:
        Vendor.objects.filter(pk=vendor.pk).update(
            on_time_delivery_rate=vendor.on_time_per,
            quality_rating_avg=vendor.quality_rat_avg,
            fulfillment_rate=vendor.fulfillment_per,
            average_response_time=vendor.avg_resp_time
        )
    return 
