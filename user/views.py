from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User

from user.serializers import UserSerializer, UserImageSerializer

from django.utils.translation import gettext_lazy as _


class CreateUSerView(generics.CreateAPIView):
    serializer_class = [UserSerializer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            department=request.data.get("department", []),
            branch=request.data.get("branch", []),
            basic_salary=request.data.get("basic_salary", []),
            role=request.data.get("role", []),
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer

        elif self.action == "upload_image":
            return UserImageSerializer

        return self.serializer_class

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerUserView(generics.RetrieveUpdateAPIView):
    serializer_class = [UserSerializer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # pagination_class = StandardResultsSetPagination

    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class LoginView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None :
            raise AuthenticationFailed(_("email or password is invalid"))
        if  not user.check_password(password):
            raise AuthenticationFailed(_("email or password is invalid"))
        refresh = RefreshToken.for_user(user)
        response = Response()
        response.data = {
            "email": user.email,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        return response


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
