from django.urls import path
from user import views

app_name = "user"
urlpatterns = [
    path("create/",views.CreateUserView.as_view(), name="create"),
    path("me/", views.ManagerUserView.as_view(), name="me"),
    path("all-users/", views.UserView.as_view(), name="view users"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LoginView.as_view(), name="logout"),
]
