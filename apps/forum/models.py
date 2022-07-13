from django.db import models
from datetime import datetime

# Create your models here.
from django.conf import settings

import apps.blog_it.models


class ForumModel(models.Model):
    tag = models.ManyToManyField("blog_it.BlogTagModel", related_name="forum_tag")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='forum', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(max_length=100, null=True)
    description = models.TextField()
    content = models.TextField()
    stt = models.IntegerField(default=1, max_length=22)
    view_count = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    notify = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, unique=True)
    time_post = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'forum'

# class EmojiModel(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emoji_author')
#     forum = models.ForeignKey(ForumModel, on_delete=models.CASCADE, related_name='forum', null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     value = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.forum.title
#
#     class Meta:
#         db_table = 'emoji'
