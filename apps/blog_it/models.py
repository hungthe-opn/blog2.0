from datetime import datetime

from django.db import models
from django.conf import settings

# Create your models here.
from apps.categorys.models import CategoryModel


class BlogTagModel(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tag'


class BlogModel(models.Model):
    tag = models.ManyToManyField(BlogTagModel, related_name="blog_tag")
    category = models.ForeignKey(CategoryModel, related_name="category", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post')
    content = models.TextField()
    slug = models.SlugField()
    stt = models.IntegerField()
    image = models.ImageField(max_length=100, null=True)
    description = models.TextField()
    source = models.CharField(max_length=255, null=True, blank=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_post = models.DateTimeField(default=datetime.now, blank=True)
    time_update = models.DateTimeField(default=datetime.now, blank=True)
    featured = models.BooleanField(default=False)
    time_read = models.CharField(default=5, max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog'


class SeriesModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    category = models.ForeignKey(CategoryModel, related_name='series_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(max_length=100, null=True)
    slug = models.SlugField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'series'


class SeriesBlogModel(models.Model):
    series = models.ForeignKey(SeriesModel, on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=250)
    image = models.ImageField(max_length=100)
    description = models.TextField(null=True)
    index = models.IntegerField(null=True)
    slug = models.SlugField()
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'series_blog'


class UpvoteModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='upvote_author')
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='blog', null=True)
    series = models.ForeignKey(SeriesModel, on_delete=models.CASCADE, related_name='upvote_series', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=1)

    def __str__(self):
        return self.blog.title

    class Meta:
        db_table = 'upvote'