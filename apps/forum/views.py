from django.shortcuts import render
from django.db.models import Q
from django.db import transaction
from datetime import date, timedelta
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.pagination import CustomPagination, PaginationAPIView
from api.utils import convert_date_front_to_back, custom_response
from .models import *
from api.permissions import IsAdmin, IsAuthor

from datetime import datetime, timedelta

# Create your views here.
from .serializers import AddBlogForumSerializer, ListBlogForumSerializer, DetailBlogForumSerializer
from ..blog_it.models import BlogTagModel, BlogModel


class AddBlogForum(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        forms = request.data
        data = {
            'author': request.user.id,
            'category': forms.get('category'),
            'title': forms.get('title'),
            'content': forms.get('content'),
            'stt': 2,
            'view_count': 0,
            'time_post': datetime.now(),
            'description': forms.get('description')
        }
        tags = forms.get('tags')
        serializer = AddBlogForumSerializer(data=data)
        if serializer.is_valid():
            blog = serializer.save()
            for tag in tags:
                tag_object = BlogTagModel.objects.filter(id=tag.get('id')).first()
                if tag_object is not None:
                    blog.tag.add(tag_object)
            return Response(custom_response(serializer.data, msg_display='Thêm bài viết thành công !'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='QUá trình thêm mới thuất bại'),
                        status=status.HTTP_400_BAD_REQUEST)


# list blog in status = 2, admin check =3
class ListBlogView(PaginationAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = BlogModel.objects.filter(stt=2)
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class DetailForumView(PaginationAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        queryset = BlogModel.objects.filter(id=pk, stt=2)
        serializer = DetailBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class ListBlogUserView(PaginationAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = BlogModel.objects.filter(id=request.user.id, stt=2)
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class ListDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        queryset = BlogModel.objects.filter(id=pk, stt=2, author_id=request.user.id)
