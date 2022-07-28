from datetime import datetime
import re
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

# Create your models here.
from apps.categorys.models import CategoryModel
from apps.comment.models import CommentModel
from apps.forum.models import ForumModel


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
    slug = models.SlugField(blank=True, unique=True)
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
        # queryset = BlogModel.objects.all().filter(slug__iexact=original_slug).count()
        # count = 1
        # slug = original_slug
        #
        # while (queryset):
        #     slug = original_slug + '-' + str(count)
        #     count += 1
        #     queryset = BlogModel.objects.all().filter(slug__iexact=slug).count()
        #
        # self.slug = slug
        #
        # if self.featured:
        #     try:
        #         temp = BlogModel.objects.get(featured=True)
        #         if self != temp:
        #             temp.featured = False
        #             temp.save()
        #     except BlogModel.DoesNotExist:
        #         pass
        # super(BlogModel, self).save(*args, **kwargs)

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
    forum = models.ForeignKey(ForumModel, on_delete=models.CASCADE, related_name='forum_upvote', null=True)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='comment_forum',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=1)

    def __str__(self):
        if self.blog is not None:
            return self.blog.title
        elif self.forum is not None:
            return self.forum.title
        else:
            return self.comment.forum.title

    class Meta:
        db_table = 'upvote'


class Bookmarks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmark_user')
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='bookmark_blog', null=True)
    forum = models.ForeignKey(ForumModel, on_delete=models.CASCADE, related_name='bookmark_forum', null=True)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.blog is not None:
            return 'Bookmarks by {} on {}'.format(self.user, self.blog)
        else:
            return 'Bookmarks by {} on {}'.format(self.user, self.forum)
