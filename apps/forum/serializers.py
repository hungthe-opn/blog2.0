from datetime import date, timedelta
from .models import *
from rest_framework import serializers

from ..blog_it.models import BlogModel
from ..blog_it.serializers import TagSerializer
from ..user.models import CreateUserModel


class AddBlogForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['author', 'category', 'title', 'image', 'description', 'content', 'stt', 'view_count',
                  'time_post']


class ListBlogForumSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()

    class Meta:
        model = ForumModel
        fields = ['id', 'tags', 'author_id', 'author_name', 'rank', 'title', 'content',
                  'slug',
                  'image', 'view_count', 'time_post', 'description', 'featured',
                  'author_email',
                  'avatar_author']

    def get_author_id(self, obj):
        return obj.author_id

    def get_author_name(self, obj):
        return obj.author.user_name

    def get_avatar_author(self, obj):
        return obj.author.image.url

    def get_rank(self, obj):
        return obj.author.rank

    def get_author_email(self, obj):
        return obj.author.email

    def get_tags(self, obj):
        tags = obj.tag.all()
        tag_serializer = TagSerializer(tags, many=True)
        return tag_serializer.data


class DetailBlogForumSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()
    upvote = serializers.SerializerMethodField()

    class Meta:
        model = ForumModel
        fields = ['id', 'tags', 'author_id', 'author_name', 'rank', 'title', 'content',
                  'slug',
                  'image', 'view_count', 'time_post', 'description', 'featured',
                  'author_email', 'upvote',
                  'avatar_author']

    def get_author_id(self, obj):
        return obj.author_id

    def get_author_name(self, obj):
        return obj.author.user_name

    def get_avatar_author(self, obj):
        return obj.author.image.url

    def get_rank(self, obj):
        return obj.author.rank

    def get_author_email(self, obj):
        return obj.author.email

    def get_upvote(self, obj):
        upvote_list = obj.forum.all()
        counter = 0
        for upvote in upvote_list:
            counter += upvote.value
        return counter
