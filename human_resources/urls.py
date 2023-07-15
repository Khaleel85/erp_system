from django.urls import path, include

# default router is used for viewsets
# from rest_framework.routers import DefaultRouter

# from human_resources.views import (
#     DepartmentViewSet,
#     BranchViewSet,
# )
from human_resources.views import (
    DepartmentCreateView,
    DepartmentListView,
    DepartmentRetrieveUpdateView,
    DepartmentDeleteView,
    BranchCreateView,
    BranchListView,
    BranchRetrieveUpdateView,
    BranchDeleteView,
)

# router = DefaultRouter()

# router.register("department", DepartmentViewSet)
# router.register("branch", BranchViewSet)


# app_name = "human_resources"

# urlpatterns = [
#     path("", include(router.urls)),


app_name = "human_resources"

urlpatterns = [
    path(
        "department/create/", DepartmentCreateView.as_view(), name="department-create"
    ),
    path("department/list/", DepartmentListView.as_view(), name="department-list"),
    path(
        "department/update/<int:pk>/",
        DepartmentRetrieveUpdateView.as_view(),
        name="department-retrieve-update",
    ),
    path(
        "department/delete/<int:pk>/",
        DepartmentDeleteView.as_view(),
        name="department-delete",
    ),
    path("branch/create/", BranchCreateView.as_view(), name="branch-create"),
    path("branch/list/", BranchListView.as_view(), name="branch-list"),
    path(
        "branch/update/<int:pk>/",
        BranchRetrieveUpdateView.as_view(),
        name="branch-retrieve-update",
    ),
    path("branch/delete/<int:pk>/", BranchDeleteView.as_view(), name="branch-delete"),
]
