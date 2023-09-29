from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.validators import username_validator
from utils.cache import get_cache
from accounts.models import UserFollow, UserContact


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64)
    username = serializers.CharField(min_length=3, max_length=64, validators=[username_validator, ])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_username(self, username):
        user = User.objects.filter(username=username)
        if user.exists():
            raise serializers.ValidationError(_('this username already exists.'))
        return username

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError(_('this email already exists.'))
        return email


class UserVerifyAccountSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4, max_length=4)

    def validate_code(self, code):
        register_info_cache = get_cache(key=code)
        if not register_info_cache:
            raise serializers.ValidationError(_('Invalid code.'))

        request = self.context['request']

        register_info_request = request.session['register_info']
        if not register_info_request:
            return serializers.ValidationError(_('Invalid code.'))

        if register_info_request['code'] != code or register_info_request['email'] != register_info_cache['email']:
            del request.session['register_info']
            raise serializers.ValidationError(_('Invalid code'))

        return code


class UserContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserContact
        fields = ('id', 'name', 'link')

        extra_kwargs = {
            "id": {"read_only": True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(method_name='get_followers_count', read_only=True)
    followings = serializers.SerializerMethodField(method_name='get_followings_count', read_only=True)
    contacts = serializers.SerializerMethodField(method_name='get_contacts', read_only=True)
    validate_edit = serializers.SerializerMethodField(method_name='check_validate_edit', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'followers', 'followings',
                  'contacts', 'validate_edit')

        extra_kwargs = {
            "email": {"read_only": True},
        }

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_contacts(self, obj):
        contacts = obj.contacts.all()
        return UserContactSerializer(instance=contacts, many=True).data

    def check_validate_edit(self, obj):
        return self.context.get('edit', False)


class UserProfileOtherSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(method_name='get_followers_count', read_only=True)
    followings = serializers.SerializerMethodField(method_name='get_followings_count', read_only=True)
    contacts = serializers.SerializerMethodField(method_name='get_contacts', read_only=True)
    validate_edit = serializers.SerializerMethodField(method_name='check_validate_edit', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'followers', 'followings',
                  'contacts', 'validate_edit')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_contacts(self, obj):
        contacts = obj.contacts.all()
        return UserContactSerializer(instance=contacts, many=True).data

    def check_validate_edit(self, obj):
        return self.context['edit']


class UserFollowerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(method_name='get_username', read_only=True)
    avatar_image = serializers.SerializerMethodField(method_name='get_avatar_image', read_only=True)

    class Meta:
        model = UserFollow
        fields = ('username', 'avatar_image')

    def get_username(self, obj):
        return obj.follower.username

    def get_avatar_image(self, obj):
        return obj.follower.avatar_image.url


class UserFollowingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(method_name='get_username', read_only=True)
    avatar_image = serializers.SerializerMethodField(method_name='get_avatar_image', read_only=True)

    class Meta:
        model = UserFollow
        fields = ('username', 'avatar_image')

    def get_username(self, obj):
        return obj.following.username

    def get_avatar_image(self, obj):
        return obj.following.avatar_image.url
