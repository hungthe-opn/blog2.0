from django.contrib import admin

# Register your models here.
from apps.comment.models import CommentModel

admin.site.register(CommentModel)
