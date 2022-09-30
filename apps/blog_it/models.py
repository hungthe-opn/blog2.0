from datetime import datetime
import re
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

# Create your models here.
from apps.categorys.models import CategoryModel
from apps.comment.models import CommentModel
from apps.forum.models import ForumModel


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(BaseModel, self).save(*args, **kwargs)


class BlogTagModel(models.Model):
    title = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_blog_tags'
        ordering = ['id']


class BlogModel(models.Model):
    tag = models.ManyToManyField(BlogTagModel, related_name="blog_tag")
    category = models.ForeignKey(CategoryModel, related_name="category", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post')
    content = models.TextField()
    slug = models.SlugField(blank=True, unique=True)
    stt = models.IntegerField()
    image = models.ImageField(max_length=1024, null=True, blank=True)
    description = models.TextField()
    source = models.CharField(max_length=255, null=True, blank=True)
    view_count = models.IntegerField(default=0)
    time_post = models.DateTimeField(default=datetime.now, blank=True)
    time_update = models.DateTimeField(default=datetime.now, blank=True)
    featured = models.BooleanField(default=False)
    time_read = models.CharField(default=5, max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.id:  # Create
            if not self.slug:  # slug is blank
                self.slug = slugify(self.title)
            else:  # slug is not blank
                self.slug = slugify(self.slug)
        else:  # Update
            self.slug = slugify(self.slug)

        qsSimilarName = BlogModel.objects.filter(slug__startswith='self.slug')
        if qsSimilarName.count() > 0:
            seqs = []
            for qs in qsSimilarName:
                seq = re.findall(r'{0:s}_(\d+)'.format(self.slug), qs.slug)
                if seq: seqs.append(int(seq[0]))
            if seqs: self.slug = '{0:s}_{1:d}'.format(self.slug, max(seqs) + 1)
        super(BlogModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_blog'
        ordering = ['id']


class SeriesModel(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    category = models.ForeignKey(CategoryModel, related_name='series_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(max_length=100, null=True)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbl_series'
        ordering = ['id']


class SeriesBlogModel(BaseModel):
    series = models.ForeignKey(SeriesModel, on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=250)
    image = models.ImageField(max_length=100)
    description = models.TextField(null=True)
    index = models.IntegerField(null=True)
    slug = models.SlugField()
    content = models.TextField(null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'tbl_series_blog'
        ordering = ['id']


class UpvoteModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='upvote_author')
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='blog', null=True, blank=True)
    series = models.ForeignKey(SeriesModel, on_delete=models.CASCADE, related_name='upvote_series', null=True, blank=True)
    forum = models.ForeignKey(ForumModel, on_delete=models.CASCADE, related_name='forum_upvote', null=True, blank=True)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='comment_forum',null=True, blank=True)
    value = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.blog is not None:
            return self.blog.title
        elif self.forum is not None:
            return self.forum.title
        else:
            return self.comment.forum.title

    class Meta:
        db_table = 'tbl_upvote'
        ordering = ['id']


class Bookmarks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmark_user')
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='bookmark_blog', null=True)
    forum = models.ForeignKey(ForumModel, on_delete=models.CASCADE, related_name='bookmark_forum', null=True)
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        if self.blog is not None:
            return 'Bookmarks by {} on {}'.format(self.user, self.blog)
        else:
            return 'Bookmarks by {} on {}'.format(self.user, self.forum)

    class Meta:
        db_table = 'tbl_bookmarks'
        ordering = ['id']
