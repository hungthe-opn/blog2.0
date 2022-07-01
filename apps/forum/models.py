from django.db import models

# Create your models here.
from django.conf import settings


class ForumModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='forum', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(max_length=100, null=True)
    description = models.TextField()
    content = models.TextField()
    stt = models.IntegerField()
    view_count = models.IntegerField()
    featured = models.BooleanField(default=False)
    notify = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'forum'
