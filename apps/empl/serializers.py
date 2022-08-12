from rest_framework import serializers

from ..blog_it.models import BlogModel
from ..user.models import CreateUserModel


class AddBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['author', 'category', 'title', 'image', 'description', 'slug', 'content', 'stt', 'view_count',
                  'source', 'time_post']


class UserRoleSerializer(serializers.ModelSerializer):
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = CreateUserModel
        fields = ['id', 'email', 'user_name', 'user_role']

    def get_user_role(self, obj):
        if obj.is_author:
            if obj.is_admin:
                role = 'admin'
            else:
                role = 'author'
        else:
            role = 'user'
        return role


class DeleteBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['id']


class EditBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['id', 'author', 'category', 'title', 'image', 'description', 'slug', 'content', 'stt',
                  'source']
