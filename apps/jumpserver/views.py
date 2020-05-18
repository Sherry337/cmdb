from django.shortcuts import render

from .models import JumpServer
from .serializers import   JumpServerSerializers
from rest_framework import viewsets,filters,status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser,DjangoObjectPermissions,DjangoModelPermissions
from rest_framework.response import Response
from utils.pagenumber import MyPageNumberPagination
# Create your views here.

class JumpServerViewSet(viewsets.ModelViewSet):
    """
    创建服务器信息
    """
    queryset = JumpServer.objects.all()
    serializer_class = JumpServerSerializers
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    # filter_class =   # 方法类过滤
    filter_fields = ("username",)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)

    # filter_fields = ("name",)   # 定义字段过滤
    permission_classes = (AllowAny,)  # 权限后需要逗号（，） 不然会报错  （不是可迭代类型）

    def get_queryset(self):
        status = self.request.GET.get('status',None)
        # print(status)
        applicant = self.request.user
        # print(applicant)
        role = applicant.groups.all().values('name')
        # print(role)
        role_name = [ r['name'] for r in role]
        # print(role_name)
        queryset = super(JumpServerViewSet, self).get_queryset()
        # print(queryset)

        # 判断传来的status值判断是申请列表还是历史列表
        if status and int(status) == 1:
            queryset = queryset.filter(status__lte=1)
        elif status and int(status) == 2:
            queryset = queryset.filter(status__exact=2)
        else:
            pass

        # 判断登陆用户是否是管理员，是则显示所有工单，否则只显示自己的
        # if "SA" not in role_name:
        #       queryset = queryset.filter(username=applicant)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        applicant = self.request.user
        # print("username", applicant)

        # 整合提交数据
        data["username"] = applicant
        data["hostname"] = data['server_name']
        data['ip'] = data['out_ip']
        data.pop("server_name")
        data.pop("out_ip")

        queryset = super(JumpServerViewSet, self).get_queryset()
        # queryset = queryset.filter(status__exact=2)
        queryset = queryset.filter(username__exact=applicant)
        old = []
        for i in queryset:
            old.append(i.ip)
        if data['ip'] not in old:
            JumpServer.objects.create(**data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # JumpServer.objects.create(**data)
        # return Response(status=status.HTTP_200_OK)
        # else:
        #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, pk=None, **kwargs):
        pk = int(pk)
        # print(pk)
        # serializer = self.get_serializer(data=request.data,)
        data = request.data
        # print(data)
        applicant = self.request.user
        # print(applicant)

        # 踢出无用数据
        data.pop("rank")
        data.pop("apply_time")
        data.pop("username")
        data.pop("ip")
        data.pop("hostname")
        #修改状态值为2，表示管理员同意授权
        data["status"] = 2
        # print(data)

        #判断用户是否为 admin
        if applicant.id == 1:
            JumpServer.objects.filter(pk=pk).update(**data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

