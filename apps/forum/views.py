from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profanity import comment_filter

from api.pagination import CustomPagination, PaginationAPIView
from api.permissions import IsAdmin
from api.utils import custom_response
# Create your views here.
from .models import ForumModel
from .serializers import AddBlogForumSerializer, ListBlogForumSerializer, DetailBlogForumSerializer, \
    UpvoteForumSerializer
from ..blog_it.models import BlogTagModel, UpvoteModel, Bookmarks
from ..blog_it.serializers import BookmarksSerializer, UserBookmarksSerializer
from ..user.models import Follow


class AddBlogForum(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        forms = request.data
        data = {
            'author': request.user.id,
            'title': forms.get('title'),
            'content': forms.get('content'),
            'stt': 3 if request.user.is_admin else 2,
            'view_count': 0,
            'time_post': datetime.now(),
            'description': forms.get('description'),
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
class PostView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        queryset = ForumModel.objects.filter(stt=3).order_by('-time_edit')
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class ListBlogViewCount(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        queryset = ForumModel.objects.filter(stt=3).order_by('-view_count')
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class DetailForumView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request, pk):
        queryset = ForumModel.objects.filter(id=pk, stt=3).first()
        bookmarks = Bookmarks.objects.filter(user=request.user.id, forum=pk)
        upvote = UpvoteModel.objects.filter(author=request.user, forum=pk).first()
        if upvote is not None:
            if upvote.value == 1:
                is_upvote = 'upvote'
            else:
                is_upvote = 'downvote'
        else:
            is_upvote = ''
        is_bookmarks = True if bookmarks.exists() else False
        serializer = DetailBlogForumSerializer(queryset)
        response = serializer.data
        response['is_bookmarks'] = is_bookmarks
        response['is_upvote'] = is_upvote
        return Response(custom_response(response), status=status.HTTP_200_OK)


class EditPostView(APIView):
    permission_classes = [IsAuthenticated | IsAdmin]

    def patch(self, request, pk):
        queryset = ForumModel.objects.filter(id=pk).first()
        forms = request.data
        data = {
            'author': request.user.id,
            'title': forms.get('title'),
            'content': comment_filter(forms.get('content')),
            'time_edit': datetime.now(),
            'description': comment_filter(forms.get('description')),
        }
        serializer = DetailBlogForumSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(serializer.data, msg_display='Chỉnh sửa bài viết thành công!'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Chỉnh sửa thuất bại. Vui lòng kiểm tra lại!'),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = ForumModel.objects.filter(id=pk)
        serializer = DetailBlogForumSerializer(queryset, many=True)
        queryset.delete()
        return Response(custom_response(serializer.data, list=False, msg_display='Xóa bài viết thành công'))


class ListBlogUserView(PaginationAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ForumModel.objects.filter(id=request.user.id, stt=2)
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class InforUser(PaginationAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, pk):
        queryset = ForumModel.objects.filter(stt=2, author_id=pk)
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class UpvoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        existing_upvote = UpvoteModel.objects.filter(author_id=request.user.id, forum_id=pk).first()
        if existing_upvote is not None:
            if existing_upvote.value == -1:
                existing_upvote.value = 1
                existing_upvote.save()
                return Response({'message': 'downvote to upvote'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'upvoted before'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "author": request.user.id,
                "forum": pk,
                "value": 1
            }
            serializer = UpvoteForumSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'err'})

    def delete(self, request, pk):
        delete_upvote = UpvoteModel.objects.filter(forum_id=pk, author_id=request.user.id)
        serializer = UpvoteForumSerializer(delete_upvote, partial=True, many=True)
        delete_upvote.delete()
        return Response(custom_response(serializer.data, list=False, msg_display='Hủy Upvote thành công'))


class DownvoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        existing_upvote = UpvoteModel.objects.filter(author_id=request.user.id, forum_id=pk).first()
        if existing_upvote is not None:
            if existing_upvote.value == 1:
                existing_upvote.value = -1
                existing_upvote.save()
                return Response({'message': 'upvote to downvote'})
            else:
                return Response({'message': 'downvoted before'})
        else:
            data = {
                "author": request.user.id,
                "forum": pk,
                "value": -1
            }
            serializer = UpvoteForumSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'err'})

    def delete(self, request, pk):
        delete_upvote = UpvoteModel.objects.filter(forum_id=pk, author_id=request.user.id)
        serializer = UpvoteForumSerializer(delete_upvote, partial=True, many=True)
        delete_upvote.delete()
        return Response(custom_response(serializer.data, list=False, msg_display='Hủy Downvote thành công'))


class ListForumFollowersView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        followings = Follow.objects.filter(from_user=request.user.id)
        followings_id = list(map(lambda x: x.to_user, followings))
        queryset = ForumModel.objects.filter(author_id__in=followings_id)
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class ListBookmarksPostView(PaginationAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Bookmarks.objects.filter(user=request.user.id)
        print(queryset)
        serializer = UserBookmarksSerializer(queryset)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class BookmarksPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = {
            'user': request.user.id,
            'forum': pk,
        }
        serializer = BookmarksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                custom_response(serializer.data, msg_display='Đã thêm bookmarks bài viết từ forum thành công !'),
                status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Thêm thuất bại'),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookmarks = Bookmarks.objects.filter(user=request.user.id, forum=pk).first()
        if bookmarks is not None:
            bookmarks.delete()
            return Response(custom_response({
                'Xóa bookmarks bài viết thành công'
            }, msg_display='Hiển thị thành công'), status=status.HTTP_200_OK)
        return Response(custom_response({}, list=False, msg_display='Quá trình đã xảy ra lỗi', response_msg='ERROR', ))
