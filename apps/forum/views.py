from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination, PaginationAPIView
from api.utils import custom_response
# Create your views here.
from .models import ForumModel
from .serializers import AddBlogForumSerializer, ListBlogForumSerializer, DetailBlogForumSerializer, \
    UpvoteForumSerializer
from ..blog_it.models import BlogTagModel, UpvoteModel
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
class ListBlogView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        queryset = ForumModel.objects.filter(stt=3).order_by('-time_post')
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class DetailForumView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request, pk):
        queryset = ForumModel.objects.filter(id=pk, stt=3).first()
        serializer = DetailBlogForumSerializer(queryset)
        return Response(custom_response(serializer.data), status=status.HTTP_200_OK)

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj


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


class ListForumFollowersView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        followings = Follow.objects.filter(from_user=request.user.id)
        followings_id = list(map(lambda x: x.to_user, followings))
        queryset = ForumModel.objects.filter(author_id__in=followings_id)
        serializer = ListBlogForumSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


# class ListForumBookmarksView(PaginationAPIView):
#     pagination_class = CustomPagination
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, pk):
#         queryset = ForumModel.objects.filter(author_id=request.user.id)
#         serializer = ListBlogForumSerializer(queryset, many=True)
#         result = self.paginate_queryset(serializer.data)
#         return self.get_paginated_response(result)
#
#     def post(self, request, pk):
#         bookmarks = ForumModel.objects.filter(author_id=request.user.id, id=pk).first()
#         data = {
#             "author": request.user.id,
#             "forum": "pk",
#             "bookmarks": True
#         }
#         serializer = ListBlogForumSerializer(bookmarks, data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(custom_response(serializer.data, msg_display='Thêm bài viết vào bookmarks thành công!'),
#                             status=status.HTTP_201_CREATED)
#         return Response(custom_response(serializer.errors, msg_display='Lỗi không thể thêm bài viết vào bookmarks'),
#                         status=status.HTTP_400_BAD_REQUEST)
