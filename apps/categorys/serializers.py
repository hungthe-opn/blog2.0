from rest_framework import serializers
from .models import CategoryModel
from api.utils import convert_date_back_to_front


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'

