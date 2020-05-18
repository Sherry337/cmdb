from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from assets.models import Servers,ServiceDirectorys
# from django.contrib.auth.models import User,Group
from rest_framework import viewsets,filters
from rest_framework.pagination import PageNumberPagination
from assets.serializers import ServersSerializers,ServiceDirSerializers
from django_filters.rest_framework import DjangoFilterBackend
from assets.filter import ServersFilter,ServiceDirectorysFilter
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser,DjangoObjectPermissions,DjangoModelPermissions
from  utils.pagenumber import MyPageNumberPagination
# from devops.permissions import IsOwnerOrReadOnly


class ServersViewSet(viewsets.ModelViewSet):
    """
    创建服务器信息
    """
    queryset = Servers.objects.all()
    serializer_class = ServersSerializers
    # pagination_class = PageNumberPagination
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ServersFilter  #方法类过滤
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('server_name','out_ip','user__chinese_name')

    # filter_fields = ("name",)   # 定义字段过滤
    permission_classes = (DjangoModelPermissions,) # 权限后需要逗号（，） 不然会报错  （不是可迭代类型）


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     创建，删除，修改，展示用户信息
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializers
#     pagination_class = PageNumberPagination
#     permission_classes = (DjangoModelPermissions,)

class ServiceDirViewSet(viewsets.ModelViewSet):
    """
    创建服务目录信息
    """
    queryset = ServiceDirectorys.objects.all()
    serializer_class = ServiceDirSerializers
    pagination_class = PageNumberPagination
    filter_class = ServiceDirectorysFilter
    permission_classes = (DjangoModelPermissions,)


# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializers
#     pagination_class = PageNumberPagination
#     permission_classes = (DjangoModelPermissions,)
