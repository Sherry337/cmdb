from rest_framework import  serializers
from business.models import Products
from django.contrib.auth.models import User


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Products
        fields = ('url','product_name','description','user')
        # fields = "__all__"



 #    def to_representation(self, instance):
 #        server = instance.server
 #        ret = super(ServiceDirectorysSerializers, self).to_representation(instance)
 #        ret["server"] = {
 #            "id": server.id,
 #            "sever_name": server.name,
 #            # "server_out_ip": server.out_ip,
 # #           "server_user": server.user_server.username
 #        }
 #        return ret
