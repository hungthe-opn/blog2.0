from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination, PaginationAPIView
from api.utils import custom_response
# Create your views here.
from apps.blog_it.models import BlogModel, UpvoteModel, BlogTagModel
from apps.blog_it.serializers import BlogSerializer, BlogDetailSerializer, UpvoteSerializer, TagSerializer


class Blog(PaginationAPIView):
    pagination_class = CustomPagination
    lookup_field = 'slug'

    def get(self, request):
        queryset = BlogModel.objects.all().order_by('-time_post')
        serializer = BlogSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class TagBlog(PaginationAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        queryset = BlogTagModel.objects.all()
        serializer = TagSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class BlogDetail(APIView):

    def get(self, request, slug):
        queryset = BlogModel.objects.get(slug=slug)
        serializer = BlogDetailSerializer(queryset)
        return Response(custom_response(serializer.data, msg_display='Hiển thị bài viết thành công!'), status=status.HTTP_200_OK)


class SearchBlogs(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']


class BlogFeatured(APIView):

    def get(self, request):
        queryset = BlogModel.objects.filter(featured=True).order_by('-time_post')
        serializer = BlogSerializer(queryset, many=True)
        return Response(custom_response(serializer.data, msg_display='Hiển thị thành công!'), status=status.HTTP_200_OK)


class UpvoteBlog(APIView):
    def post(self, request, pk):
        existing_upvote = UpvoteModel.objects.filter(author_id=request.user.id, blog_id=pk).first()
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
                "blog": pk,
                "value": 1
            }
            serializer = UpvoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'Lỗi trong quá trình Upvote'})


class DownVoteBlog(APIView):
    def post(self, request, pk):
        existing_upvote = UpvoteModel.objects.filter(author_id=request.user.id, blog_id=pk).first()
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
                "blog": pk,
                "value": -1
            }
            serializer = UpvoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'Lỗi trong quá trình Downvote'})


class CountBlog(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = BlogModel.objects.filter(author_id=request.user.id)
        total_blogs = blogs.count()
        total_views = sum(list(map(lambda blog: blog.view_count, blogs)))
        return Response({
            'data': {
                'total_views': total_views,
                'total_blogs': total_blogs,
            }
        }
        )


class ListCategoryView(PaginationAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, pk):
        queryset = BlogModel.objects.filter(category_id=pk)
        serializer = BlogSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)


class ListTagView(PaginationAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, pk):
        queryset = BlogModel.objects.filter(tag_id=pk)
        serializer = BlogSerializer(queryset, many=True)
        result = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(result)
