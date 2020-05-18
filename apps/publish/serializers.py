from rest_framework import  serializers
from .models import Project, Deploy

from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Project
        # fields = ()
        fields =  "__all__"

    def to_dev_user_response(self,user_queryset):
        ret = []
        for i in user_queryset:
            ret.append({
                'id': i.id,
                'user': i.chinese_name
            })
        return ret

    def to_audit_user_response(self,user_queryset):
        ret = []
        for i in user_queryset:
            ret.append({
                'id': i.id,
                'user': i.chinese_name
            })
        return ret

    def to_release_user_response(self,user_queryset):
        ret = []
        for i in user_queryset:
            ret.append({
                'id': i.id,
                'user': i.chinese_name
            })
        return ret

    def to_representation(self, instance):
        dev_user = self.to_dev_user_response(instance.dev_user.all())
        audit_user = self.to_audit_user_response(instance.audit_user.all())
        release_user = self.to_release_user_response(instance.release_user.all())
        ret = super(ProjectSerializers, self).to_representation(instance)
        ret["dev_user"] = dev_user
        ret["audit_user"] = audit_user
        ret["release_user"] = release_user
        return ret

class DeploySerializers(serializers.ModelSerializer):
    class Meta:
        model  = Deploy
        # fields = ()
        fields =  "__all__"

    def to_apply_user_response(self, user_queryset):
        try:
            return {
                "id": user_queryset.id,
                "user": user_queryset.chinese_name
            }
        except Exception as e:
            return {}

    def to_reviewer_user_response(self, user_queryset):
        try:
            return {
                "id": user_queryset.id,
                "user": user_queryset.chinese_name
            }
        except Exception as e:
            return {}

    def to_assign_user_response(self, user_queryset):
        try:
            return {
                "id": user_queryset.id,
                "user": user_queryset.chinese_name
            }
        except Exception as e:
            return {}


    def to_representation(self, instance):
        applicant = self.to_apply_user_response(instance.applicant)
        reviewer = self.to_reviewer_user_response(instance.reviewer)
        assign_to = self.to_assign_user_response(instance.assign_to)
        ret = super(DeploySerializers, self).to_representation(instance)
        ret["applicant"] = applicant
        ret["reviewer"] = reviewer
        ret["assign_to"] = assign_to
        return ret

    # def partial_update(self, validated_data):
    #     validated_data["is_active"] = True
    #     validated_data["password"] = "12345678"
    #     instance = super(UserSerializer, self).create(validated_data=validated_data)
    #     instance.email = "{}{}".format(instance.username, settings.DOMAIN)
    #     instance.set_password(validated_data["password"])