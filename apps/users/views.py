from django.shortcuts import render

from assets.models import Servers,ServiceDirectorys
from django.contrib.auth.models import Group,Permission
# from users.models import User
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from users.serializers import UserSerializers,GroupSerializers,PermissionSerializer
from django_filters.rest_framework import DjangoFilterBackend
# from assets.filter import ServersFilter,ServiceDirectorysFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser,DjangoObjectPermissions,DjangoModelPermissions
# Create your views here.
from rest_framework import viewsets, mixins, permissions,status,filters
from utils.pagenumber import MyPageNumberPagination


from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    创建，删除，修改，展示用户信息
    """
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = MyPageNumberPagination
    permission_classes = (DjangoModelPermissions,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username','chinese_name')


class UserInfoViewset(viewsets.ViewSet):
    """
    获取当前登陆的用户信息
    """
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        data = {
            "id": self.request.user.id,
            "username": self.request.user.username,
            "name": self.request.user.chinese_name
        }
        return Response(data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers
    pagination_class = MyPageNumberPagination
    permission_classes = (DjangoModelPermissions,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)


# 定制分页
class DefaultPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
    max_page_size = 1000

class PermissionsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = DefaultPagination
    permission_classes = (DjangoModelPermissions,)


class UserGroupsViewset(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    """
    update:
    修改指定用户的角色
    """
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (DjangoModelPermissions,)

    queryset = User.objects.all()
    serializer_class = UserSerializers

    # 重写update方法，只针对用户和组进行单独的处理，类似的场景还有修改密码，更改状态等
    def update(self, request, *args, **kwargs):
        # print(request.data)
        # print(self.get_object())
        user_obj = self.get_object()
        roles = request.data.get("role", [])
        # print(roles)
        # user_obj.groups = roles
        user_obj.groups.set(roles)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupsPermViewset(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    """
    update:
    修改指定角色的权限
    """
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (DjangoModelPermissions,)

    queryset = Group.objects.all()
    serializer_class = GroupSerializers

    def update(self, request, *args, **kwargs):
        group_obj = self.get_object()
        power = request.data.get("power", [])
        # print(power)
        group_obj.permissions.set(power)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMembersViewset(mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    destroy:
    从指定组里删除指定成员
    """
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (DjangoModelPermissions,)

    queryset = Group.objects.all()
    serializer_class = GroupSerializers

    def destroy(self, request, *args, **kwargs):
        # print(self.get_object())
        # print(request.data)
        group_obj = self.get_object()
        uid = request.data.get('uid', 0)
        group_obj.user_set.remove(int(uid))
        return Response(status=status.HTTP_200_OK)