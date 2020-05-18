from django.shortcuts import render

from rest_framework.response import Response
from .serializers import WorkorderSerializers
from .models import Workorder
from rest_framework import viewsets,filters,status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser,DjangoObjectPermissions,DjangoModelPermissions
from utils.pagenumber import MyPageNumberPagination
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class WorkorderViewSet(viewsets.ModelViewSet):

    queryset = Workorder.objects.all()
    serializer_class = WorkorderSerializers
    pagination_class = MyPageNumberPagination
    permission_classes = (DjangoModelPermissions,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('work_name', )

    def get_queryset(self):
        status = self.request.GET.get('status',None)
        # print(status)
        applicant = self.request.user
        # print(applicant)
        role = applicant.groups.all().values('name')
        # print(role)
        role_name = [ r['name'] for r in role]
        # print(role_name)
        queryset = super(WorkorderViewSet, self).get_queryset()
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
        #       queryset = queryset.filter(applicant=applicant)
        return queryset

    def partial_update(self, request, *args, pk=None, **kwargs):

        pk = int(pk)
        # print(pk)
        # serializer = self.get_serializer(data=request.data,)

        data = request.data
        # print(data)

        if data['status'] == 1:

            data['status'] = 2
            applicant = self.request.user
            # print(applicant.id)
            stop_time = datetime.datetime.now()

            data['stop_time'] = stop_time
            data['manager_user'] = applicant
            data['status'] = 2

            data.pop("work_name")
            data.pop('content')
            data.pop('start_time')
            # print(data)
            # print(data['status'])

            Workorder.objects.filter(pk=pk).update(**data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            pass
