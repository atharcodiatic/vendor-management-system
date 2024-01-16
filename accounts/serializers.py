from rest_framework import serializers
from .models import *
import uuid
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

class VendorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='enter password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = Vendor
        exclude = ["last_login", "groups", "user_permissions", "is_staff", 
                   "is_active", "is_superuser" , "date_joined" , "vendor_code"]
        
    def create(self,validated_data):
        vendor_obj = Vendor.objects.create_user(**validated_data)
        vendor_obj.save()
        return vendor_obj
        
class VendorLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
        

        
    
