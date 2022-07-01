from datetime import datetime

from django.db import models
from apps.blog_it.models import BlogModel
# Create your models here.
from django.conf import settings

from apps.forum.models import ForumModel


class CommentModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment', on_delete=models.CASCADE)
    forum = models.ForeignKey(ForumModel, related_name='forum', on_delete=models.CASCADE)
    icon = models.CharField(max_length=10, null=True)
    time_comment = models.DateTimeField(default=datetime.now, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author

    class Meta:
        db_table = 'comment'


