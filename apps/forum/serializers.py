from rest_framework import serializers

from .models import *
from ..blog_it.models import UpvoteModel
from ..blog_it.serializers import TagSerializer


class AddBlogForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumModel
        fields = ['author', 'title', 'image', 'description', 'content', 'stt', 'view_count',
                  'time_post', 'slug']


class ListBlogForumSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()
    upvote = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = ForumModel
        fields = ['id', 'tags', 'author_id', 'author_name', 'rank', 'title', 'content',
                  'slug', 'upvote', 'comment',
                  'image', 'view_count', 'time_post', 'description', 'featured',
                  'author_email',
                  'avatar_author', 'created_at']

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

    def get_upvote(self, obj):
        upvote_list = obj.forum_upvote.all()
        counter = 0
        for upvote in upvote_list:
            counter += upvote.value
        return counter

    def get_comment(self, obj):
        comment_list = obj.forum.all().count()
        return comment_list


class DetailBlogForumSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()
    upvote = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    quantity_comments = serializers.SerializerMethodField()

    class Meta:
        model = ForumModel
        fields = ['id', 'tags', 'author_id', 'author_name', 'rank', 'title', 'content',
                  'slug',
                  'image', 'view_count', 'time_post', 'description', 'featured',
                  'author_email', 'upvote', 'quantity_comments',
                  'avatar_author', 'created_at','updated_at']

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
        upvote_list = obj.forum_upvote.all()
        counter = 0
        for upvote in upvote_list:
            counter += upvote.value
        return counter

    def get_tags(self, obj):
        tags = obj.tag.all()
        tag_serializer = TagSerializer(tags, many=True)
        return tag_serializer.data

    def get_view_count(self,obj):
        obj.view_count += 1
        obj.save()
        return obj.view_count

    def get_quantity_comments(self,obj):
        quantity = obj.forum.filter(reply_of=None).count()
        return quantity


class UpvoteForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpvoteModel
        fields = ('id', 'author', 'forum', 'series', 'value', 'comment')
