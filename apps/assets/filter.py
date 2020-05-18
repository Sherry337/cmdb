import django_filters
from assets.models import Servers,ServiceDirectorys


class ServersFilter(django_filters.FilterSet):
    class Meta:
        model = Servers
        fields = ['server_name','out_ip','user']

class ServiceDirectorysFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceDirectorys
        fields = ['prot']
