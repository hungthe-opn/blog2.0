from django.db import models

from apps.comment.models import CommentModel
from apps.forum.models import ForumModel
from apps.user.models import CreateUserModel, Follow
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


# Create your models here.
class NotificationModel(models.Model):
    from_user = models.ForeignKey(CreateUserModel, related_name='noti_fr_user', on_delete=models.CASCADE, null=True)
    to_user = models.ForeignKey(CreateUserModel, related_name='noti_to_user', on_delete=models.CASCADE, null=True)
    to_forum = models.ForeignKey(ForumModel, related_name='noti_to_forum', on_delete=models.CASCADE, null=True)
    to_follow = models.ForeignKey(Follow, related_name='noti_to_follow', on_delete=models.CASCADE, null=True)
    to_comment = models.ForeignKey(CommentModel, related_name='noti_to_comment', on_delete=models.CASCADE, null=True)
    is_upvote = models.BooleanField(default=False)
    is_comment = models.BooleanField(default=False)
    is_following = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    enable = models.BooleanField(default=True)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_notifications'
        unique_together = ['from_user', 'to_user']

    def __str__(self):
        if self.to_follow is not None:
            return f"{self.from_user.user_name} started following {self.to_user.user_name}"
        elif self.to_comment is not None:
            return f"{self.from_user.user_name} reply comment {self.to_comment.forum.title} of {self.to_user.user_name}"
        else:
            return f"Notify:{self.from_user.user_name} upvote blogs {self.to_forum.title}  "

    def save(self, *args, **kwargs):
        channels_layer = get_channel_layer()
        request = kwargs.get('request', None)
        notification_obj = NotificationModel.objects.filter(enable=True).count()

        data = {'count': notification_obj, 'current_notify': self.content, 'link': self.link}
        print('data', data)
        async_to_sync(channels_layer.group_send)(
            'test_consumers_group', {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )
        super(NotificationModel, self).save(*args, **kwargs)
