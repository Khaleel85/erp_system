from django.urls import path, include

from rest_framework.routers import DefaultRouter

from human_resources.views import (
    DepartmentViewSet,
    BranchViewSet,
    LoanViewSet,
    PayRollViewSet,
    PermissionViewSet,
    GroupViewSet,
    RoleViewSet,
)

router = DefaultRouter()

router.register("department", DepartmentViewSet)
router.register("branch", BranchViewSet)
router.register("apply-loan", LoanViewSet)
router.register("pay-roll", PayRollViewSet)
router.register("user-permissions", PermissionViewSet)
router.register("group", GroupViewSet)
router.register("role", RoleViewSet)

app_name = "human_resources"

urlpatterns = [
    path("", include(router.urls)),
]
