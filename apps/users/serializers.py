from rest_framework import  serializers
from django.contrib.auth.models import Group,Permission,ContentType
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()



class UserSerializers(serializers.ModelSerializer):
    """
    用户序列化
    """

    class Meta:
        model  = User
        fields = ('url','id','username','chinese_name','email',"is_active")
        # fields = "__all__"
    def to_group_response(self,group_queryset):
        ret = []
        for group in group_queryset:
            ret.append({
                'id': group.id,
                'name': group.name
            })
        return ret

    def to_representation(self, instance):
        role = self.to_group_response(instance.groups.all())
        ret = super(UserSerializers, self).to_representation(instance)
        ret['role'] = role
        return ret

    def create(self, validated_data):
        validated_data["is_active"] = True
        validated_data["password"] = "12345678"
        instance = super(UserSerializers, self).create(validated_data=validated_data)
        # instance.email = "{}{}".format(instance.username, settings.DOMAIN)
        # print(validated_data["password"])
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
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

class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name')


    def to_permission_response(self, permission_queryset):
        ret = []
        # 将角色权限信息序列化
        for permission in permission_queryset:
            ret.append({
                'id': permission.id,
                'name': permission.name,
                'codename': permission.codename,
            })
        return ret

    def to_members_response(self, members_queryset):
        ret = []
        # 将角色用户信息序列化
        for member in members_queryset:
            ret.append({
                'id': member.id,
                'username': member.username,
                'name': member.chinese_name,
            })
        return ret

    def to_representation(self, instance):
        members = self.to_members_response(instance.user_set.all())
        number = instance.user_set.count()
        power = self.to_permission_response(instance.permissions.all())
        ret = super(GroupSerializers, self).to_representation(instance)
        ret["members"] = members
        ret["number"] = number
        ret["power"] = power
        return ret


class PermissionSerializer(serializers.ModelSerializer):
    # content_type = ContentTypeSerializer()

    class Meta:
        model = Permission
        fields = ("id", "name", "codename")