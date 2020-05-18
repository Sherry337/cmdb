import django_filters
from business.models import Products



class ProductsFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ["product_name",]

