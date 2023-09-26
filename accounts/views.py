from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from accounts.serializers import (UserRegisterSerializer, UserProfileSerializer,
                                  UserVerifyAccountSerializer,)
from accounts.services import user_register, create_user_from_cache


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_register(**serializer.validated_data, request=request)
        return Response(status=status.HTTP_201_CREATED)


class UserVerifyAccountView(APIView):
    serializer_class = UserVerifyAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        create_user_from_cache(code=serializer.validated_data['code'])
        return Response(status=status.HTTP_200_OK)


class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
