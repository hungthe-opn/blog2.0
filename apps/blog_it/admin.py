from django.contrib import admin

# Register your models here.
from apps.blog_it.models import BlogTagModel, BlogModel, SeriesModel, SeriesBlogModel, UpvoteModel
from django.apps import apps

app = apps.get_app_config('blog_it')

for model_name, model in app.models.items():
    admin.site.register(model)
