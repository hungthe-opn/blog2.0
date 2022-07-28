from rest_framework import serializers
from apps.comment.models import CommentModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['forum', 'icon', 'body', 'active', 'created_at', 'updated_at', 'author', 'reply_of']


class RepCommentSerializer(serializers.ModelSerializer):
    author_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = ['id', 'author', 'forum', 'icon', 'body', 'active', 'created_at', 'updated_at', 'reply_of',
                  'author_id', 'author_name', 'rank', 'avatar_author']

    def get_author_id(self, obj):
        return obj.author.id

    def get_author_name(self, obj):
        return obj.author.user_name

    def get_rank(self, obj):
        return obj.author.rank

    def get_avatar_author(self, obj):
        return obj.author.image.url

    def create(self, validated_data):
        comment_id = validated_data.get('reply_of')
        if comment_id is None:
            return False
        else:
            comment = CommentModel.objects.create(**validated_data)
            return comment


class ListCommentSerializer(serializers.ModelSerializer):
    author_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    avatar_author = serializers.SerializerMethodField()
    quantity_upvote = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = ['id', 'author', 'forum', 'icon', 'body', 'active', 'created_at', 'updated_at', 'reply_of',
                  'quantity_upvote',
                  'author_id', 'author_name', 'rank', 'avatar_author']

    def get_author_id(self, obj):
        return obj.author.id

    def get_author_name(self, obj):
        return obj.author.user_name

    def get_rank(self, obj):
        return obj.author.rank

    def get_avatar_author(self, obj):
        return obj.author.image.url

    def get_quantity_upvote(self, obj):
        upvote_list = obj.comment_forum.all()
        counter = 0
        for upvote in upvote_list:
            counter += upvote.value
        return counter


