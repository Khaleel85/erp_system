from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from human_resources.serializers import (
    DepartmentSerializer,
    BranchSerializer,
)

from core.pagination import StandardResultsSetPagination
from core.models import (
    Department,
    Branch,
)


# class DepartmentViewSet(viewsets.ModelViewSet):
#     serializer_class = DepartmentSerializer
#     queryset = Department.objects.all()
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardResultsSetPagination

#     def get_queryset(self):
#         return self.queryset.order_by("id")

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class DepartmentCreateView(generics.CreateAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class DepartmentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class DepartmentDeleteView(generics.DestroyAPIView):
    queryset = Department.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


# class BranchViewSet(viewsets.ModelViewSet):
#     serializer_class = BranchSerializer
#     queryset = Branch.objects.all()
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardResultsSetPagination

#     def get_queryset(self):
#         return self.queryset.order_by("id")


#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
class BranchCreateView(generics.CreateAPIView):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BranchListView(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class BranchRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class BranchDeleteView(generics.DestroyAPIView):
    queryset = Branch.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
