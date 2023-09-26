from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.validators import username_validator
from utils.cache import get_cache


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


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
