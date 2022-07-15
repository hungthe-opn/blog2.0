from rest_framework import serializers

from apps.comment.models import CommentModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['author', 'forum', 'icon', 'body', 'active', 'created_at', 'updated_at']


class RepCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentModel
        fields = ['id', 'author', 'forum', 'icon', 'body', 'active', 'created_at', 'updated_at', 'reply_of']
