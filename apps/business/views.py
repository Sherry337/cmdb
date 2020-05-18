from django.shortcuts import render

from business.models import Products
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from business.serializers import ProductsSerializers
from django_filters.rest_framework import DjangoFilterBackend
from business.filter import ProductsFilter
from rest_framework.permissions import IsAuthenticated,AllowAny

# Create your views here.

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializers
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductsFilter
    permission_classes = (IsAuthenticated,)

