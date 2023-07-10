from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class CustomJWTAuthentication(JWTTokenUserAuthentication):
    def get_header(self, request):
        return None

    def get_raw_token(self, request):
        return request.data.get(
            "token"
        )  # Change "token" to match the field name in the request body
