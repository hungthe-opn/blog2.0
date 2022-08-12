from django.urls import path
from .views import Blog, BlogDetail, UpvoteBlog, DownVoteBlog, CountBlog, BlogFeatured, TagBlog, \
    ListCategoryView, ListTagView, SearchBlogs

app_name = 'blog_it'

urlpatterns = [
    path('', Blog.as_view(), name='list-blog'),
    path('tag/', TagBlog.as_view(), name='tag'),
    path('upvote/<int:pk>', UpvoteBlog.as_view(), name='upvote'),
    path('downvote/<int:pk>', DownVoteBlog.as_view(), name='down_vote'),
    path('featured/', BlogFeatured.as_view(), name='blog-detail'),
    path('count/', CountBlog.as_view(), name='count-blog'),
    path('category/<pk>', ListCategoryView.as_view(), name='blog-category'),
    path('tag/<pk>', ListTagView.as_view(), name='blog-tag'),
    path('slug/<str:slug>/', BlogDetail.as_view(), name='blog-detail'),
    path('search/', SearchBlogs.as_view(), name='search-post'),

]
