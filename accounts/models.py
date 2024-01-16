from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import MinLengthValidator
# Create your models here.

class Vendor(AbstractUser):
    first_name = None
    last_name = None

    email = models.EmailField(_("email address"), unique=True,)
    name = models.CharField(max_length = 50) # Vendor's name.
    contact_details = models.TextField() #- Contact information of the vendor.
    address = models.TextField()  #- Physical address of the vendor.
    vendor_code = models.CharField(max_length=80, unique= True) # - A unique identifier for the vendor.
    on_time_delivery_rate = models.FloatField(default = 0.0 , validators = [MinLengthValidator(0.0)]) # - Tracks the percentage of on-time deliveries.
    quality_rating_avg = models.FloatField(default = 0.0 , validators = [MinLengthValidator(0.0)]) # - Average rating of quality based on purchase orders.
    average_response_time = models.FloatField(default = 0.0,validators = [MinLengthValidator(0.0)]) # - Average time taken to acknowledge purchase orders.
    fulfillment_rate = models.FloatField(default = 0.0, validators = [MinLengthValidator(0.0)]) #Percentage of purchase orders fulfilled successfully

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
