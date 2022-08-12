from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAdmin, IsAuthor
from api.utils import custom_response
from apps.blog_it.models import BlogModel, BlogTagModel
from apps.blog_it.serializers import BlogSerializer
from apps.empl.serializers import AddBlogSerializer, UserRoleSerializer, DeleteBlogSerializer, EditBlogSerializer
from apps.user.models import CreateUserModel


class AddBlog(APIView):
    permission_classes = [IsAdmin | IsAuthor]

    def post(self, request, *args, **kwargs):
        forms = request.data
        data = {
            'author': request.user.id,
            'category': forms.get('category'),
            'title': forms.get('title'),
            'content': forms.get('content'),
            'image': forms.get('image'),
            'stt': 1,
            'view_count': 0,
            'source': forms.get('source'),
            'time_post': datetime.now(),
            'description': forms.get('description')
        }
        tags = forms.get('tags')
        serializer = AddBlogSerializer(data=data)
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


class UpdateBlog(APIView):
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


class UserRole(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = CreateUserModel.objects.filter(id=request.user.id).first()
        serializer = UserRoleSerializer(queryset)
        return Response(custom_response(serializer.data, msg_display='Hiển thị thành công'),
                        status=status.HTTP_201_CREATED)


class DeleteExport(APIView):
    permission_classes = [IsAdmin | IsAuthor]

    def delete(self, request, pk):
        queryset = BlogModel.objects.filter(id=pk)
        serializer = DeleteBlogSerializer(queryset)
        queryset.delete()
        return Response(custom_response(serializer.data, list=False, msg_display='Xóa bài viết thành công'))


class UpdateInsurance(APIView):
    permission_classes = [IsAdmin | IsAuthor]

    def patch(self, request, pk, *args, **kwargs):
        queryset = BlogModel.objects.filter(id=pk).first()
        data = {
            'category': request.data.get('category'),
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'slug': request.data.get('slug'),
            'content': request.data.get('content'),
            'source': request.data.get('source'),
            'time_update':datetime.now()
        }
        serializer = EditBlogSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Cập nhật bài viết thuất bại, vui lòng thử lại sau'),
                        status=status.HTTP_400_BAD_REQUEST)
