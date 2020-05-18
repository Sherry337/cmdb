from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet,DeployViewSet

publish_router = DefaultRouter()
# publish_router.register(r'status', JenkinsViewset, base_name="status")
publish_router.register(r'project', ProjectViewSet, base_name="project")
publish_router.register(r'deploy', DeployViewSet, base_name="deploy")