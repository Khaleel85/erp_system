from django.urls import path, include

from rest_framework.routers import DefaultRouter

from human_resources.views import (
    DepartmentViewSet,
    BranchViewSet,
)

router = DefaultRouter()

router.register("department", DepartmentViewSet)
router.register("branch", BranchViewSet)


app_name = "human_resources"

urlpatterns = [
    path("", include(router.urls)),
]
