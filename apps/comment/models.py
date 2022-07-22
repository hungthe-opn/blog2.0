# Create your models here.
from django.conf import settings
from django.db import models

from apps.forum.models import ForumModel


class CommentModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment', on_delete=models.CASCADE)
    forum = models.ForeignKey(ForumModel, related_name='forum', on_delete=models.CASCADE)
    icon = models.CharField(max_length=10, null=True)
    body = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply_of = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.forum)

    class Meta:
        db_table = 'comment'
