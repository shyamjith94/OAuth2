from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from accesstoken.serializers import RefreshTokenSerializer, UserLoginSerializer


class UserLoginView(RetrieveAPIView):
    """
    required username, password
    return access token, refreshToken
    payload -
            {
                "username": "shyam",
                "password": "asd123##"
            }
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data["username"])
        refresh_token = RefreshToken.for_user(user)
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "User logged in  successfully",
            "access_token": serializer.data["token"],
            "refresh_token": str(refresh_token),
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class RefreshTokenView(TokenRefreshView):
    """
    required refresh token
    return access token, refreshToken
    payload -
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVz
        aCIsImV4cCI6MTYyMDIyNTE4MCwianRpIjoiMTFmZDBjODY5Y2U5NGVhMjk5OTBlZDY2MTFlM2M4
        YzgiLCJ1c2VyX2lkIjoyfQ.-9jnyVfTKRDH1I0-jQZtnGGZP6LbhL7JecaBeh3g4f4"
    }
    """

    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer
