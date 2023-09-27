from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from accounts.serializers import (UserRegisterSerializer, UserProfileSerializer,
                                  UserVerifyAccountSerializer,)
from accounts.services import (user_register, create_user_from_cache, get_user_by_username,
                               user_follow, user_unfollow)


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


class UserFollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        user = get_user_by_username(username=username)
        if user is None:
            return Response(data={"data": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)
        if user.id == request.user.id:
            return Response(data={"data": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)
        user_follow(follower=request.user, following=user)
        return Response(status=status.HTTP_200_OK)


class UserUnfollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        user = get_user_by_username(username=username)
        if user is None:
            return Response(data={"data": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)
        if user.id == request.user.id:
            return Response(data={"data": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)
        user_unfollow(follower=request.user, following=user)
        return Response(status=status.HTTP_200_OK)


class UserFollowerListView(APIView):

    def get(self, request):
        pass


class UserFollowingListView(APIView):

    def get(self, request):
        pass
