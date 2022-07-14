from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTagModel
        fields = ('id', 'title',)


class BlogSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()
    # tag_name = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()

    # upvote = serializers.SerializerMethodField()

    class Meta:
        model = BlogModel
        fields = ['id', 'tags', 'author_id', 'author_name', 'category_id', 'rank', 'category_name', 'title', 'content',
                  'slug', 'time_read',
                  'image', 'source', 'view_count', 'time_post', 'time_update', 'description', 'featured',
                  'author_email',
                  'avatar_author']
        lookup_field = 'slug'

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

    def get_category_id(self, obj):
        return obj.category_id

    def get_category_name(self, obj):
        return obj.category.name

    def get_tags(self, obj):
        tags = obj.tag.all()
        tag_serializer = TagSerializer(tags, many=True)
        return tag_serializer.data


class BlogDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    upvote = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = BlogModel
        fields = ['id', 'author_id', 'author_name', 'category_id', 'rank', 'category_name', 'title', 'content', 'slug',
                  'author_email',
                  'avatar_author', 'time_read', 'tags',
                  'image', 'source', 'view_count', 'time_post', 'time_update', 'upvote', 'description', 'featured']
        lookup_field = 'slug'

    def get_author_id(self, obj):
        return obj.author_id

    def get_author_email(self, obj):
        return obj.author.email

    def get_author_name(self, obj):
        return obj.author.user_name

    def get_rank(self, obj):
        return obj.author.rank

    def get_category_id(self, obj):
        return obj.category_id

    def get_category_name(self, obj):
        return obj.category.name

    def get_upvote(self, obj):
        upvote_list = obj.blog.all()
        counter = 0
        for upvote in upvote_list:
            counter += upvote.value
        return counter

    def get_avatar_author(self, obj):
        return obj.author.image.url

    def get_tags(self, obj):
        tags = obj.tag.all()
        tag_serializer = TagSerializer(tags, many=True)
        return tag_serializer.data

    def get_view_count(self,obj):
        obj.view_count +=1
        obj.save()
        return obj


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpvoteModel
        fields = ('id', 'author', 'blog', 'series', 'value')


class QuantityBlogSerializer(serializers.ModelSerializer):
    category_quantity = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = BlogModel
        fields = ['id', 'category_name', 'category_quantity']

    def get_category_quantity(self, obj):
        quantity = obj.category.category.all().count()
        return quantity

    def get_category_name(self, obj):
        return obj.category.name
