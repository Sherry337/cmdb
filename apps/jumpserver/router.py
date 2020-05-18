from rest_framework.routers import DefaultRouter
from .views import JumpServerViewSet

jumpserver_router = DefaultRouter()
# publish_router.register(r'status', JenkinsViewset, base_name="status")
jumpserver_router.register(r'jumpserver', JumpServerViewSet, base_name="jumpserver")
