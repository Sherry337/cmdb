from rest_framework import  serializers
from .models import Workorder

from django.contrib.auth import get_user_model

User = get_user_model()


class WorkorderSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Workorder
        # fields = ()
        fields =  "__all__"

    def to_manager_user_response(self, user_queryset):
        try:
            return {
                "id": user_queryset.id,
                "user": user_queryset.chinese_name
            }
        except Exception as e:
            return {}


    def to_representation(self, instance):
        manager_user = self.to_manager_user_response(instance.manager_user)
        ret = super(WorkorderSerializers, self).to_representation(instance)
        ret["manager_user"] = manager_user
        return ret

