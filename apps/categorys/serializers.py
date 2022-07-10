from rest_framework import serializers
from .models import CategoryModel
from api.utils import convert_date_back_to_front
from ..blog_it.models import BlogModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class CategoryBlogsSerializer(serializers.ModelSerializer):
    counter = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'slug', 'counter']

    def get_counter(self, obj):
        post = obj.all().filter(id__category=id)
        post_count = post.count()
        return post_count

