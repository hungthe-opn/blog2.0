from rest_framework import serializers

from .models import *
from ..blog_it.models import UpvoteModel, Bookmarks
from ..blog_it.serializers import TagSerializer
from ..comment.models import CommentModel


class AddBlogForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumModel
        fields = ['author', 'title', 'image', 'description', 'content', 'stt', 'view_count',
                  'time_edit', 'slug']


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
                  'image', 'view_count', 'time_edit', 'description', 'featured',
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
    points = serializers.SerializerMethodField()
    reputation = serializers.SerializerMethodField()
    follower_counter = serializers.SerializerMethodField()

    class Meta:
        model = ForumModel
        fields = ['id', 'tags', 'author_id', 'author_name', 'rank', 'title', 'content',
                  'slug',
                  'image', 'view_count', 'time_edit', 'description', 'featured',
                  'author_email', 'upvote', 'quantity_comments', 'points',
                  'reputation', 'follower_counter',
                  'avatar_author', 'created_at', 'time_edit']

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

    def get_view_count(self, obj):
        obj.view_count += 1
        obj.save()
        return obj.view_count

    def get_quantity_comments(self, obj):
        quantity = obj.forum.filter(reply_of=None).count()
        return quantity

    def get_follower_counter(self, obj):
        return obj.author.followers.count()

    def get_points(self, obj):
        comment_counter = CommentModel.objects.filter(author=obj.author_id).count()
        post_counter = ForumModel.objects.filter(author=obj.author_id).count()
        forum_upvotes = UpvoteModel.objects.filter(forum__author=obj.author_id)
        forum_bookmarks = Bookmarks.objects.filter(forum__author=obj.author_id)
        blog_upvotes = UpvoteModel.objects.filter(blog__author=obj.author_id)
        forum_upvote_counter = sum(list(map(lambda upvote: upvote.value, forum_upvotes)))
        forum_bookmarks_couter = sum(list(map(lambda bookmark: bookmark.count, forum_bookmarks)))
        blog_upvote_counter = sum(list(map(lambda upvote: upvote.value, blog_upvotes)))
        return comment_counter * 1 + post_counter * 2 + forum_upvote_counter * 1 + blog_upvote_counter * 1 + forum_bookmarks_couter * 0.5

    def get_reputation(self, obj):
        followers_counter = obj.author.followers.count()
        forum_upvotes = UpvoteModel.objects.filter(forum__author=obj.author_id)
        forum_upvote_counter = sum(list(map(lambda upvote: upvote.value, forum_upvotes)))
        return followers_counter * 2 + forum_upvote_counter * 1


class UpvoteForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpvoteModel
        fields = ('id', 'author', 'forum', 'series', 'value', 'comment')


class CheckStatusBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = ['id', 'author', 'forum', 'created_at', 'updated_at', 'count']
