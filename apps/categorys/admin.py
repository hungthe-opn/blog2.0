from django.contrib import admin

# Register your models here.
from apps.blog_it.models import CategoryModel

admin.site.register(CategoryModel)
