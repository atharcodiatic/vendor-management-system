from django.dispatch import receiver
from django.db.models.signals import  post_save, pre_save
from .models import *
import uuid 

@receiver(pre_save, sender= Vendor)
def generate_vendor_code(sender, instance,**kwargs):
    if not instance.vendor_code:
        vendor_code = uuid.uuid4().__str__()
        instance.vendor_code = vendor_code
    return