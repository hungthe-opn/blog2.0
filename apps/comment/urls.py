from django.urls import path
from .views import CommentBlogView,RepCommentView


app_name = 'comments'

urlpatterns = [
    path('<pk>/', CommentBlogView.as_view(), name='comment'),
    path('reply/<pk>/', RepCommentView.as_view(), name='comment'),

]