from datetime import date, timedelta
from .models import *
from rest_framework import serializers

from ..blog_it.models import BlogModel
from ..user.models import CreateUserModel


class AddBlogForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['author', 'category', 'title', 'image', 'description', 'content', 'stt', 'view_count',
                  'time_post']
