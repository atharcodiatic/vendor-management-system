from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import *
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer , TemplateHTMLRenderer
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError , InvalidToken

class VendorViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsOwnerAction]


class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = VendorLoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    

    




