from django.contrib.auth.models import update_last_login
from django.db import transaction, DatabaseError
from requests import Response
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
import models
from api import errors, constant
from api.logger import logger_raise_warn_exception
from .models import CreateUserModel, Follow
from ..blog_it.models import UpvoteModel, Bookmarks
from ..comment.models import CommentModel
from ..forum.models import ForumModel


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if len(attrs.keys()) == 0:
            logger_raise_warn_exception(attrs, errors.RequireValue, detail="ペイロードが空です", code=305)

        email = attrs.get('email')
        password = attrs.get('password')
        if email is not None:
            is_username_existed = CreateUserModel.objects.filter(email=email, delete=False).exists()
            if is_username_existed:
                logger_raise_warn_exception(self.initial_data, errors.ExistedValue,
                                            detail="同じメールアドレスの顧客が既に登録されています", code=306)
            else:
                attrs['email'] = email

        if password.isalnum():
            logger_raise_warn_exception(self.initial_data, errors.FormatErrorValue,
                                        detail="パスワードには特殊文字が必要です", code=403)
        else:
            attrs['password'] = password
        return attrs

    def create(self, validated_data):
        try:
            password = validated_data.pop('password', None)
            current_username = validated_data.get('user_name', None)
            if len(current_username) > 5:
                instance = self.Meta.model(**validated_data)
                if password is not None:
                    instance.set_password(password)
                instance.save()
            else:
                return ''
            return instance
        except Exception as e:
            print('ERR', e)


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
    follower_counter = serializers.SerializerMethodField()
    following_counter = serializers.SerializerMethodField()
    quantity_comments = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    reputation = serializers.SerializerMethodField()

    class Meta:
        model = CreateUserModel
        fields = ['id', 'email', 'user_name', 'first_name', 'start_date', 'about', 'rank', 'image', 'sex',
                  'follower_counter', 'following_counter', 'quantity_comments', 'points', 'reputation']

    def get_follower_counter(self, obj):
        return obj.followers.count()

    def get_following_counter(self, obj):
        return obj.followings.count()

    def get_quantity_comments(self, obj):
        quantity = obj.comment.all().count()
        return quantity

    def get_points(self, obj):
        comment_counter = CommentModel.objects.filter(author=obj).count()
        post_counter = ForumModel.objects.filter(author=obj).count()
        forum_upvotes = UpvoteModel.objects.filter(forum__author=obj)
        forum_bookmarks = Bookmarks.objects.filter(forum__author=obj)
        blog_upvotes = UpvoteModel.objects.filter(blog__author=obj)
        forum_upvote_counter = sum(list(map(lambda upvote: upvote.value, forum_upvotes)))
        forum_bookmarks_couter = sum(list(map(lambda bookmark: bookmark.count, forum_bookmarks)))
        print(forum_bookmarks_couter)
        blog_upvote_counter = sum(list(map(lambda upvote: upvote.value, blog_upvotes)))
        return comment_counter * 1 + post_counter * 2 + forum_upvote_counter * 1 + blog_upvote_counter * 1 + forum_bookmarks_couter * 0.5

    def get_reputation(self, obj):
        followers_counter = obj.followers.count()
        forum_upvotes = UpvoteModel.objects.filter(forum__author=obj)
        forum_upvote_counter = sum(list(map(lambda upvote: upvote.value, forum_upvotes)))
        return followers_counter * 2 + forum_upvote_counter * 1


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['to_user', 'from_user', 'created']


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
    follower_counter = serializers.SerializerMethodField()
    following_counter = serializers.SerializerMethodField()

    # is_following = serializers.SerializerMethodField()

    class Meta:
        model = CreateUserModel
        fields = ['id', 'email', 'user_name', 'first_name', 'start_date', 'about', 'rank', 'image', 'sex',
                  'follower_counter', 'following_counter']

    def get_follower_counter(self, obj):
        return obj.followers.count()

    def get_following_counter(self, obj):
        return obj.followings.count()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = [
            'id', 'user_name', 'first_name', 'about', 'groups', 'delete', 'is_admin', 'is_author', ''
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = constant.DEFAULT_USER_DATA

    def validate(self, attrs):
        if len(attrs.keys()) == 0:
            logger_raise_warn_exception(attrs, errors.RequireValue, detail="ペイロードが空です", code=305)
        email = attrs.get('email')
        password = attrs.get('password')
        user_name = attrs.get('user_name')
        if email is not None:
            is_email_existed = CreateUserModel.objects.filter(email=email, delete=False).exists()
            is_username_existed = CreateUserModel.objects.filter(user_name=user_name, delete=False).exists()
            if is_email_existed:
                logger_raise_warn_exception(self.initial_data, errors.ExistedValue,
                                            detail="同じメールアドレスの顧客が既に登録されています", code=306)
            else:
                attrs['email'] = email
                if is_username_existed:
                    logger_raise_warn_exception(self.initial_data, errors.ExistedValue,
                                                detail="同じメールアドレスの顧客が既に登録されています", code=306)
                else:
                    attrs['user_name'] = user_name
                    attrs['password'] = password
        else:
            logger_raise_warn_exception(self.initial_data, errors.RequireValue, detail="emailは必須項目です。", code=307)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            if password.isalnum():
                logger_raise_warn_exception(self.initial_data, errors.ExistedValue,
                                            detail="同じメールアドレスの顧客が既に登録されています", code=306)
            else:
                instance.set_password(password)
        instance.save()
        return instance
