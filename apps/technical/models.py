from django.db import models
from django.conf import settings

from apps.forum.models import ForumModel


class BaseTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
# Create your models here.


class TagTechnicalModel(models.Model):
    title = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='technical_user')
    forum = models.ForeignKey(ForumModel, on_delete=models.CASCADE, related_name='follow_technical', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'technical_tbl'

    def __str__(self):
        return 'Title: {} in Technical'.format(self.title)

