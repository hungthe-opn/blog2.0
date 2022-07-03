from django.shortcuts import render
from rest_framework.views import APIView
from api.pagination import CustomPagination, PaginationAPIView
from api.utils import convert_date_front_to_back, custom_response
from datetime import date, timedelta
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
from apps.blog_it.models import BlogModel
from apps.blog_it.serializers import BlogSerializer


class BlogView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        queryset = BlogModel.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)
