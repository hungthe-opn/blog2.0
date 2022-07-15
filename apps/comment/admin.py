from django.contrib import admin

# Register your models here.
from apps.comment.models import CommentModel


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'forum', 'icon', 'active')
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('author', 'icon', 'body')
