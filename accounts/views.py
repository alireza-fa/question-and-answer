from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from accounts.serializers import (UserRegisterSerializer, UserProfileSerializer,
                                  UserVerifyAccountSerializer, UserFollowerSerializer,
                                  UserFollowingSerializer, UserContactSerializer,
                                  UserProfileOtherSerializer,)
from accounts.services import (user_register, create_user_from_cache, get_user_by_username,
                               user_follow, user_unfollow, get_followers, get_followings,
                               user_contact_create, get_user_contact,)
from accounts.paginations import FollowPagination


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


class UserProfileEditView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data, instance=request.user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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


class UserProfileOtherView(APIView):
    serializer_class_other = UserProfileOtherSerializer
    serializer_class_self = UserProfileSerializer

    def get(self, request, username):
        user = get_user_by_username(username=username)
        if user is None:
            return Response(data={"detail": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user=user)(
            instance=user, context={"edit": self.check_validated_edit(user=user)})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def check_validated_edit(self, user: object) -> bool:
        if self.request.user == user:
            return True
        return False

    def get_serializer(self, user: object):
        if self.request.user == user:
            return self.serializer_class_self
        return self.serializer_class_other


class ContactCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserContactSerializer

    def post(self, request):
        contacts = request.user.contacts.all()

        if contacts.count() >= 4:
            return Response(
                data={"detail": _('User can not more than 4 contact link.')}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        user_contact_create(user=request.user, name=vd['name'], link=vd['link'])
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserContactDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, contact_id):
        user_contact = get_user_contact(contact_id=contact_id, user=request.user)
        if user_contact is None:
            return Response(data={"detail": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)
        user_contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollowerListView(APIView):
    pagination_class = FollowPagination
    serializer_class = UserFollowerSerializer

    def get(self, request, username):
        user = get_user_by_username(username=username)
        if user is None:
            return Response(data={"detail": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)

        followers = get_followers(user=user)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset=followers, request=request)
        serializer = self.serializer_class(instance=paginated_queryset, many=True)
        return paginator.get_paginated_response(data=serializer.data)


class UserFollowingListView(APIView):
    pagination_class = FollowPagination
    serializer_class = UserFollowingSerializer

    def get(self, request, username):
        user = get_user_by_username(username=username)
        if user is None:
            return Response(data={"detail": _('Not found.')}, status=status.HTTP_404_NOT_FOUND)

        followers = get_followings(user=user)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset=followers, request=request)
        serializer = self.serializer_class(instance=paginated_queryset, many=True)
        return paginator.get_paginated_response(data=serializer.data)
