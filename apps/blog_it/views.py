from django.shortcuts import render
from rest_framework.views import APIView
from api.pagination import CustomPagination, PaginationAPIView
from api.utils import convert_date_front_to_back, custom_response
from datetime import date, timedelta
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from api.permissions import IsAdmin, IsReport

# Create your views here.
from apps.blog_it.models import BlogModel, UpvoteModel
from apps.blog_it.serializers import BlogSerializer, BlogDetailSerializer, UpvoteSerializer


class BlogView(PaginationAPIView):
    pagination_class = CustomPagination
    # permission_classes = [IsAdmin]

    def get(self, request):
        queryset = BlogModel.objects.all().order_by('-time_post')
        serializer = BlogSerializer(queryset, many=True)
        print(serializer)
        result = self.paginate_queryset(serializer.data)
        print(result)

        return self.get_paginated_response(result)


class BlogDetailView(APIView):
    # permission_classes = [IsReport | IsAdmin]

    def get(self, request, pk):
        queryset = BlogModel.objects.filter(id=pk).order_by('-time_post').first()
        queryset.view_count += 1
        queryset.save()
        serializer = BlogDetailSerializer(queryset)
        return Response(custom_response(serializer.data), status=status.HTTP_201_CREATED)


class UpvoteView(APIView):
    def post(self, request, pk):
        existing_upvote = UpvoteModel.objects.filter(author_id=request.user.id, blog_id=pk).first()
        if existing_upvote is not None:
            if existing_upvote.value == -1:
                existing_upvote.value = 1
                existing_upvote.save()
                return Response({'message': 'downvote to upvote'})
            else:
                return Response({'message': 'upvoted before'})
        else:
            data = {
                "author": request.user.id,
                "blog": pk,
                "value": 1
            }
            serializer = UpvoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'message': 'err'})


class DownvoteView(APIView):
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
                return Response(serializer.data)
            return Response({'message': 'err'})