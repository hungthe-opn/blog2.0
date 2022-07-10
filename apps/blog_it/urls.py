from django.urls import path
from .views import BlogView, BlogDetailView, UpvoteView, DownvoteView, CountBlogView,ListFeaturedView

app_name = 'blog_it'

urlpatterns = [
    path('', BlogView.as_view(), name='blog-list'),
    path('<pk>', BlogDetailView.as_view(), name='blog-detail'),
    path('upvote/<int:pk>', UpvoteView.as_view(), name='upvote'),
    path('downvote/<int:pk>', DownvoteView.as_view(), name='down_vote'),
    path('featured/', ListFeaturedView.as_view(), name='blog-detail'),
    path('count/', CountBlogView.as_view(), name='count-blog'),
]
