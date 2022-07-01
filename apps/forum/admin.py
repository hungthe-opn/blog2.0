from django.contrib import admin

# Register your models here.
from apps.forum.models import ForumModel

admin.site.register(ForumModel)
