from django.urls import path
from .views import BlogView, BlogDetailView, UpvoteView, DownvoteView

app_name = 'blog_it'

urlpatterns = [
    path('', BlogView.as_view(), name='blog-list'),
    path('<pk>', BlogDetailView.as_view(), name='blog-detail'),
    path('upvote/<int:pk>', UpvoteView.as_view(), name='upvote'),
    path('downvote/<int:pk>', DownvoteView.as_view(), name='downvote'),
    path('downvote/<int:pk>', DownvoteView.as_view(), name='downvote'),

]
