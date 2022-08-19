from django.contrib import admin

# Register your models here.
from apps.forum.models import ForumModel


@admin.register(ForumModel)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('author', 'id', 'title')

