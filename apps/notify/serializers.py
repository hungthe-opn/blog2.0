from rest_framework import serializers

from .models import *


class ForumNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = (
            'id',
            'from_user',
            'to_forum', 'enable', 'content', 'is_upvote',
                                             'link', 'is_following', 'is_comment',
            'created_at', 'updated_at')
