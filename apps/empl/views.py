from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.pagination import CustomPagination, PaginationAPIView
from api.utils import convert_date_front_to_back, custom_response
from datetime import date, timedelta, datetime
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from api.permissions import IsAdmin, IsReport, IsAuthor

from apps.blog_it.models import BlogModel, UpvoteModel
from apps.blog_it.serializers import BlogSerializer
from apps.empl.serializers import AddBlogSerializer, UserRoleSerializer
from apps.user.models import CreateUserModel


class AddBlogView(APIView):
    permission_classes = [IsAdmin | IsAuthor]

    def post(self, request, *args, **kwargs):
        forms = request.data
        data = {
            'author': request.user.id,
            'category': forms.get('category'),
            'title': forms.get('title'),
            'slug': forms.get('slug'),
            'content': forms.get('content'),
            'image': forms.get('image'),
            'stt': 1,
            'view_count': 0,
            'source': forms.get('source'),
            'time_post': datetime.now(),
            'description': forms.get('description')
        }
        serializer = AddBlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(serializer.data, msg_display='Thêm bài viết thành công !'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='QUá trình thêm mới thuất bại'),
                        status=status.HTTP_400_BAD_REQUEST)


class UpdateBlogView(APIView):
    permission_classes = [IsAdmin | IsAuthor]

    def patch(self, request, pk):
        queryset = BlogModel.objects.filter(id=pk).first()
        forms = request.data
        data = {
            'title': forms.get('title'),
            'content': forms.get('content'),
            'slug': forms.get('slug'),
            'image': forms.get('image'),
            'source': forms.get('source'),
            'description': forms.get('description'),
            'time_update': datetime.now()
        }
        serializer = BlogSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(serializer.data, msg_display='Chỉnh sửa bài viết thành công!'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Chỉnh sửa thuất bại. Vui lòng kiểm tra lại!'),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = BlogModel.objects.filter(id=pk)
        serializer = BlogSerializer(queryset, partial=True, many=True)
        queryset.delete()
        return Response(custom_response(serializer.data, list=False, msg_display='Xóa bài viết thành công'))


class UserRoleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = CreateUserModel.objects.filter(id=request.user.id).first()
        serializer = UserRoleSerializer(queryset)
        return Response(custom_response(serializer.data, msg_display='Hiển thị thành công'),
                        status=status.HTTP_201_CREATED)