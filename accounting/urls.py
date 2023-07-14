from django.urls import path
from accounting.views import (
    LedgerEntryListView,
    LedgerEntryCreateView,
    LedgerEntryRetrieveView,
    LedgerEntryUpdateView,
)

urlpatterns = [
    path("ledger-lists/", LedgerEntryListView.as_view(), name="ledger-entry-list"),
    path(
        "ledger-entries/", LedgerEntryCreateView.as_view(), name="ledger-entry-create"
    ),
    path(
        "ledger-entries/<int:pk>/",
        LedgerEntryRetrieveView.as_view(),
        name="ledger-entry-retrieve-update",
    ),
    path(
        "ledger-entries/<int:pk>/",
        LedgerEntryUpdateView.as_view(),
        name="ledger-entry-retrieve-update",
    ),
]
