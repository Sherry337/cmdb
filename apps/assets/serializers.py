from rest_framework import  serializers
from assets.models import Servers,ServiceDirectorys
#
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()
from business.models import Products


class ServiceDirSerializers(serializers.ModelSerializer):
    class Meta:
        model  = ServiceDirectorys
        fields = ('url','directory','prot','start_way','description','server')
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


class ServersSerializers(serializers.ModelSerializer):
    """"
    Cmdb 序列化
    """
    # id                  = serializers.IntegerField(read_only=True)
    # only_id             = serializers.CharField(required=True,max_length=255)
    # name                = serializers.CharField(required=True,max_length=255)
    # out_ip              = serializers.CharField(required=True,max_length=20)
    # in_ip               = serializers.CharField(required=True,max_length=20)
    # os                  = serializers.CharField(required=True,max_length=255)
    # yun_company         = serializers.CharField(required=True,max_length=255)
    #server_directory = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    # 第一种方法
    # 增加 ServiceDirectorysSerializers 表信息
    # servers = ServiceDirectorysSerializers(many=True,required=False)

    class Meta:
        model  = Servers
        fields = ('url','server_name','out_ip','in_ip','os','yun_company','env','district','user','product')
        # depth = 1
        # fields  = "__all__"

    # def validate(self, attrs):
    #     servers = attrs['servers']
    #     del attrs['servers']


    # def to_representation(self, instance):
    #     user_server = instance.user_server
    #     ret = super(ServerSerializers, self).to_representation(instance)
    #     ret["user_server"] = {
    #         "id": user_server.id,
    #         "server": user_server.username,
    #     }
    #     return ret

    #第二种方法
    def get_server_user(self,user_obj):
        try:
            return {
                "user": user_obj.chinese_name
            }
        except Exception as e:
            return {}

    def get_service_directorys(self,server_obj):
        ret = []
        service_dir = server_obj.servers_servicedir.all()
        for servicedir in service_dir:
            data = {
                "directory": servicedir.directory,
                "prot": servicedir.prot,
                "start_way": servicedir.start_way,
                "description": servicedir.description
            }
            ret.append(data)
        return ret

    def get_product_name(self,server_obj):
        try:
            return {
                "product": server_obj.product_name
            }
        except Exception as e:
            return {}

    def to_representation(self, instance):
        server_user = self.get_server_user(instance.user)
        servicedirectory = self.get_service_directorys(instance)
        product_name = self.get_product_name(instance.product)
        # print(instance.user_server)
        ret = super(ServersSerializers, self).to_representation(instance)
        ret["user"] = server_user
        ret["servicedir"] = servicedirectory
        ret["product"] = product_name
        return ret


# class UserSerializers(serializers.ModelSerializer):
#     class Meta:
#         model  = User
#         fields = ('url','username','email')


# class ServiceDirectorysSerializers(serializers.ModelSerializer):
#     class Meta:
#         model  = ServiceDirectorys
#         fields = ('url','directory','prot','description','server')
#
#     def to_representation(self, instance):
#         server = instance.server
#         ret = super(ServiceDirectorysSerializers, self).to_representation(instance)
#         ret["server"] = {
#             "id": server.id,
#             "sever_name": server.name,
#             "server_out_ip": server.out_ip,
#  #           "server_user": server.user_server.username
#         }
#         return ret

# class GroupSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')
