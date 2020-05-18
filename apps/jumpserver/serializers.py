from rest_framework import  serializers
from .models import JumpServer

from django.contrib.auth import get_user_model

User = get_user_model()


class JumpServerSerializers(serializers.ModelSerializer):
    class Meta:
        model  = JumpServer
        # fields = ()
        fields =  "__all__"

    # def to_user(self, user_queryset):
    #     try:
    #         return {
    #             "id": user_queryset.id,
    #             "user": user_queryset.username,
    #             "chinese_name": user_queryset.chinese_name
    #         }
    #     except Exception as e:
    #         return {}
    #
    # def to_server_ip(self, server_queryest):
    #     try:
    #         return {
    #             "id": server_queryest.id,
    #             "ip": server_queryest.out_ip
    #         }
    #     except Exception as e:
    #         return {}
    #
    # def to_server_hostname(self, server_queryest):
    #     try:
    #         return {
    #             "id": server_queryest.id,
    #             "server_name": server_queryest.server_name
    #         }
    #     except Exception as e:
    #         return {}
    #
    #
    # def to_representation(self, instance):
    #     user = self.to_user(instance.username)
    #     ip = self.to_server_ip(instance.ip)
    #     hostname = self.to_server_hostname(instance.hostname)
    #     ret = super(JumpServerSerializers, self).to_representation(instance)
    #     ret["username"] = user
    #     ret["ip"] = ip
    #     ret["hostname"] = hostname
    #     return ret
