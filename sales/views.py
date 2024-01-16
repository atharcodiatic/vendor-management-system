from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer , TemplateHTMLRenderer
from django.contrib.auth import authenticate, login
# Create your views here.

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self):
        update_methods = ["PUT", "PATCH"]
        if self.request.method in update_methods:
            pk = self.kwargs.get('pk')
            if PurchaseOrder.objects.filter(id=pk).exists():
                purchase_obj = PurchaseOrder.objects.get(id=pk)
                if not purchase_obj.delivery_date:
                    return PurchaseOrderUpdateSerializer
                elif not purchase_obj.quality_rating and purchase_obj.delivery_date and purchase_obj.status =='completed':
                    return QualityRatingSerializer
                else:
                    return StatusUpdateSerializer
            else:
                return super().get_serializer_class()
        else:
            return self.serializer_class
        
class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer