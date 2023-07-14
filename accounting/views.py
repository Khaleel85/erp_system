from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework import generics

from core.models import LedgerEntry
from core.pagination import StandardResultsSetPagination

from serializers import LedgerEntrySerializer


class LedgerEntryListView(generics.ListAPIView):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = [StandardResultsSetPagination]


class LedgerEntryCreateView(generics.CreateAPIView):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = [StandardResultsSetPagination]


class LedgerEntryUpdateView(generics.UpdateAPIView):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = [StandardResultsSetPagination]


class LedgerEntryRetrieveView(generics.RetrieveAPIView):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = [StandardResultsSetPagination]
