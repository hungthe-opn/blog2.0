from django.urls import path
from .views import CommentBlogView


app_name = 'comments'

urlpatterns = [
    path('<pk>/', CommentBlogView.as_view(), name='comment'),
]