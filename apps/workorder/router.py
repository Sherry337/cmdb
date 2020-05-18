from rest_framework.routers import DefaultRouter
from .views import WorkorderViewSet

workorder_router = DefaultRouter()
workorder_router.register(r'workorder', WorkorderViewSet, base_name="workorder")
