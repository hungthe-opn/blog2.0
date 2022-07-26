from rest_framework.response import Response
from datetime import date

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.pagination import CustomPagination, PaginationAPIView

from api.utils import custom_response
from apps.blog_it.models import UpvoteModel
from apps.comment.models import CommentModel
from apps.comment.serializers import CommentSerializer, ListCommentSerializer, RepCommentSerializer
from apps.forum.serializers import UpvoteForumSerializer
from profanity import comment_filter


class CommentBlogView(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request, pk):
        queryset = CommentModel.objects.filter(forum=pk).order_by('-created_at')
        author_comment = CommentModel.objects.filter(author=request.user.id)
        is_comment = True if author_comment.exists() else False
        serializer = ListCommentSerializer(queryset, many=True)
        response = serializer.data
        for i in range(len(response)):
            response[i]['is_comment'] = is_comment
        result = self.paginate_queryset(response)
        return self.get_paginated_response(result)

    def post(self, request, pk):
        forms = request.data
        data = {
            'author': request.user.id,
            'forum': pk,
            'icon': forms.get('icon'),
            'body': comment_filter(forms.get('body')),
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(serializer.data, msg_display='Thêm bình luận thành công!'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Bình luận thuất bại, vui lòng thử lại'),
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        queryset = CommentModel.objects.filter(id=pk, author_id=request.user.id).first()
        forms = request.data

        data = {
            'body': comment_filter(forms.get('body')),
        }
        serializer = ListCommentSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                custom_response(serializer.data, msg_display='Chỉnh sửa thành công.'),
                status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Chỉnh sửa thành công'),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = CommentModel.objects.filter(id=pk, author_id=request.user.id)
        serializer = RepCommentSerializer(queryset, partial=True, many=True)
        queryset.delete()
        return Response(custom_response(serializer.data, list=False, msg_display='Xóa bài viết thành công'))


class RepCommentView(APIView):

    def post(self, request, pk):
        comment = CommentModel.objects.filter(id=pk, reply_of=None).first()
        forms = request.data
        data = {
            'author': request.user.id,
            'forum': pk,
            'icon': forms.get('icon'),
            'body': comment_filter(forms.get('body')),
            'reply_of': forms.get('reply_of')
        }
        serializer = RepCommentSerializer(comment,data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(custom_response(serializer.data, msg_display='Thêm bình luận thành công!'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Bình luận thuất bại, vui lòng thử lại'),
                        status=status.HTTP_400_BAD_REQUEST)


class UpVoteComment(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        existing_upvote = UpvoteModel.objects.filter(author_id=request.user.id, comment_id=pk).first()
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
                "comment": pk,
                "value": 1
            }
            serializer = UpvoteForumSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'err'})


class DownVoteComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        existing_upvote = UpvoteModel.objects.filter(author_id=request.user.id, comment_id=pk).first()
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
                "comment": pk,
                "value": -1
            }
            serializer = UpvoteForumSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'err'})

