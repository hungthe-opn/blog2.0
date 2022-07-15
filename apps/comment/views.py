from rest_framework.response import Response
from datetime import date

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import custom_response
from apps.comment.models import CommentModel
from apps.comment.serializers import CommentSerializer


class CommentBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        forms = request.data
        data = {
            'author': request.user.id,
            'forum': pk,
            'icon': forms.get('icon'),
            'body': forms.get('body'),

        }
        serializer = CommentSerializer( data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(serializer.data, msg_display='Thêm bình luận thành công!'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Bình luận thuất bại, vui lòng thử lại'),
                        status=status.HTTP_400_BAD_REQUEST)

