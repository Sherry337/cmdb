"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path,include
from django.conf.urls import url
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

from assets.views import ServersViewSet,ServiceDirViewSet
from users.views import UserViewSet,GroupViewSet,UserInfoViewset,PermissionsViewset,UserGroupsViewset,GroupMembersViewset,GroupsPermViewset
from business.views import ProductsViewSet
from publish.views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r'servers',ServersViewSet)
router.register(r'users',UserViewSet)
router.register(r'servicedirectorys',ServiceDirViewSet)
router.register(r'products',ProductsViewSet)
router.register(r'group',GroupViewSet)
router.register(r'userinfo',UserInfoViewset, base_name="userinfo")
router.register(r'permission',PermissionsViewset, base_name="permission")
router.register(r'usergroup',UserGroupsViewset,base_name="usergroup")
router.register(r'groupmembers',GroupMembersViewset,base_name="groupmembers")
router.register(r'grouppower',GroupsPermViewset,base_name="grouppower")
# router.register(r'project1',ProjectViewSet,base_name="project1")
# router.register(r'users',UserViewSet)

from users.router import users_router
from publish.router import publish_router
from workorder.router import workorder_router
from jumpserver.router import  jumpserver_router

router.registry.extend(users_router.registry)
router.registry.extend(publish_router.registry)
router.registry.extend(workorder_router.registry)
router.registry.extend(jumpserver_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/',include(router.urls)),
    url(r'^docs/',include_docs_urls("中通国际AIP文档")),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    url(r'^api/v1/api-token-auth/', obtain_jwt_token),
    # url(r'^api-token-refresh/', refresh_jwt_token),
]
