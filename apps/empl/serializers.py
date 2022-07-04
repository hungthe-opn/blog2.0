from datetime import date, timedelta
from .models import *
from rest_framework import serializers

from ..blog_it.models import BlogModel


class AddBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['author', 'category', 'title', 'image', 'description', 'slug', 'content', 'stt', 'view_count',
                  'source', 'time_post']
