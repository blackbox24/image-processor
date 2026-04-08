from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer


class SignUpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get("username", "")
            password = data.get("password", "")

            user = User.objects.create_user(username=username, password=password)

            token = RefreshToken.for_user(user)
            return Response(
                {"username": username, "id": user.pk, "token": str(token.access_token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
