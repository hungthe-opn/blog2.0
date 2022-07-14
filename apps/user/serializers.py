from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CreateUserModel, Follow


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UpdateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = ('id', 'user_name', 'first_name', 'about', 'image')



class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = ['id', 'email', 'user_name', 'first_name', 'start_date', 'about', 'rank', 'image', 'sex']


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'from_user', 'created']


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'to_user', 'created']


class UserFollowSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = CreateUserModel
        fields = ['id', 'email', 'user_name', 'rank', 'image', 'start_date', 'about', 'from_user', 'to_user']
        extra_kwargs = {"password": {"write_only": True}}

    def get_from_user(self, obj):
        return obj.follower.id

    def get_to_user(self, obj):
        return obj.follow_target.id


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = ['id', 'email', 'user_name', 'first_name', 'start_date', 'about', 'rank', 'image', 'sex']