from django.shortcuts import render
from rest_framework.response import Response
from .serializers import ProjectSerializers, DeploySerializers
from .models import Project, Deploy

from rest_framework import viewsets,filters,status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from assets.filter import ServersFilter,ServiceDirectorysFilter
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser,DjangoObjectPermissions,DjangoModelPermissions
import datetime
from time import  sleep,time
from utils.jenkins_api import JenkinsApi
from .tasks import release_code
# from .tasks import add
from django.contrib.auth import get_user_model
from utils.pagenumber import MyPageNumberPagination

User = get_user_model()
# Create your views here.


import jenkins



class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    pagination_class = MyPageNumberPagination
    permission_classes = (DjangoModelPermissions,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('project_name', )

# class JenkinsViewset(viewsets.ViewSet):
#     def jenkins_connet(self, request, *args, **kwargs):
#         server = jenkins.Jenkins('http://127.0.0.1:8080', username="zl", password="123456")
#         status = request.data.get("status")
#         print(status)
#         if status == 1:
#             server.build_job("my_test")
#         else:
#             pass
#         return Response(status)
# 定制分页
class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
    max_page_size = 100

class DeployViewSet(viewsets.ModelViewSet):

    queryset = Deploy.objects.all()
    serializer_class = DeploySerializers
    pagination_class = DefaultPagination
    permission_classes = (DjangoModelPermissions,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )

    def get_queryset(self):
        status = self.request.GET.get('status',None)
        # print(status)
        applicant = self.request.user
        # print(applicant)
        role = applicant.groups.all().values('name')
        # print(role)
        role_name = [ r['name'] for r in role]
        # print(role_name)
        queryset = super(DeployViewSet, self).get_queryset()
        # print(queryset)

        # 判断传来的status值判断是申请列表还是历史列表
        if status and int(status) <= 3:
            queryset = queryset.filter(status__lte=3)
        elif status and int(status) == 4:
            queryset = queryset.filter(status__exact=4)
        else:
            pass

        # 判断登陆用户是否是管理员，是则显示所有工单，否则只显示自己的
        # if "SA" not in role_name:
        #       queryset = queryset.filter(applicant=applicant)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        # print(data)
        project_user = Project.objects.filter(project_name=data["project_name"]).values("dev_user")
        project_name = [r['dev_user'] for r in project_user]
        # print(project_user)
        # print(project_name)
        applicant = self.request.user
        # print(applicant.id)
        role = applicant.groups.all().values('name')
        # print(role)
        role_name = [r['name'] for r in role]
        # user_id = User.objects.filter(username = applicant)
        # if "DEV" in role_name and:
        if  (applicant.id  in project_name and "DEV" in role_name) or "SA" in role_name:
            data["applicant"] = applicant
            Deploy.objects.create(**data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, pk=None, **kwargs):

        pk = int(pk)
        # print(pk)
        # serializer = self.get_serializer(data=request.data,)

        data = request.data
        # print(data)



        if data['status'] == 2:

            project_user = Project.objects.filter(project_name=data["project_name"]).values("audit_user")
            project_name = [r['audit_user'] for r in project_user]
            # print(project_user)
            # print(project_name)
            applicant = self.request.user
            # print(applicant.id)
            role = applicant.groups.all().values('name')
            # print(role)
            role_name = [r['name'] for r in role]

            data.pop("project_name")
            # print(data)
            # print(data['status'])

            if  (applicant.id  in project_name and "PMO" in role_name) or "SA" in role_name:
                Deploy.objects.filter(pk=pk).update(**data)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif data['status'] == 3:

            project_user = Project.objects.filter(project_name=data["project_name"]).values("release_user")
            project_name = [r['release_user'] for r in project_user]
            # print(project_user)
            # print(project_name)
            applicant = self.request.user
            # print(applicant.id)
            role = applicant.groups.all().values('name')
            # print(role)
            role_name = [r['name'] for r in role]

            #手动更新发布时间
            deploy_time = datetime.datetime.now()
            # print(deploy_time)
            data['deploy_time'] = deploy_time

            #增加权控制，必须是 项目列表中的人员并且 在对应组中。SA 有所有权限

            if (applicant.id in project_name and "QA" in role_name) or "SA" in role_name:

                 jenkins = JenkinsApi()
                 #当前的构建号
                 number = jenkins.get_next_build_number(data['project_name'])
                 project_name = data['project_name']
                # print(type(number))
                 #print(number)
                 # jenkins.build_job(data['project_name'], parameters={'tag': data['version']})
                 #进行发布操作
                 jenkins.build_job(data['project_name'])
                 #查询发布返回值
                 # sleep(30)
                 # start_time = time()
                 # while True:
                 #    if (jenkins.get_build_info(project_name, number)) == "SUCCESS":
                 #        data["release_status"] = 1
                 #        break
                 #    elif (jenkins.get_build_info(project_name, number)) == "ABORTED":
                 #        data["release_status"] = 3
                 #        break
                 #    elif (jenkins.get_build_info(project_name, number)) == "FAILURE" or (time() - start_time) > 60:
                 #        data["release_status"] = 2
                 #        break

                 release_code.delay(pk, project_name, number)
                 # add.delay(1,4)
                 # release_code.delay(pk,data)
                 # 弹出项目名，因为不需要修改
                 data.pop("project_name")
                 # print(data)
                 # print(type(data))
                 # print(data)


                 # sleep(30)
                 # console_output = jenkins.get_build_console_output(data['name'], number)
                 # data['console_output'] = console_output
                 # print('2222')

                 Deploy.objects.filter(pk=pk).update(**data)
                 # sleep(20)
                 # while (jenkins.get_build_info(project_name, number)) != "SUCCESS":
                 #    print(1)
                 return Response(status=status.HTTP_204_NO_CONTENT)

            # else:
            #     pass
                # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            pass

         # if data['status'] == 3:
         #     jenkins = JenkinsApi()
         #     number = jenkins.get_next_build_number(data['name'])
         #     jenkins.build_job(data['name'], parameters={'tag': data['version']})
         #     sleep(30)
         #     console_output = jenkins.get_build_console_output(data['name'], number)
         #     data['console_output'] = console_output
         #     print('2222')
         # Deploy.objects.filter(pk=pk).update(**data)
         # return Response(status=status.HTTP_204_NO_CONTENT)



    # def update(self, request, *args, **kwargs):
    #     pk = int(kwargs.get("pk"))
    #     data = (request.data).dict()
    #     print(data)
    #     print(data['name'])
    #     print(data['version'])
    #     jenkins = JenkinsApi()
    #     number = jenkins.get_next_build_number(data['name'])
    #     jenkins.build_job(data['name'], parameters={'tag': data['version']})
    #     sleep(10)
    #     # console_output = jenkins.get_build_console_output(data['name'], number)
    #     # data['console_output'] = console_output
    #     print(data)
    #     Deploy.objects.filter(pk=pk).update(**data)
    #     return Response(status=status.HTTP_204_NO_CONTENT)