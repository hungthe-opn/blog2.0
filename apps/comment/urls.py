from django.urls import path

from .views import CommentBlogView, RepCommentView,UpVoteComment,DownVoteComment

app_name = 'comments'

urlpatterns = [
    path('<pk>/', CommentBlogView.as_view(), name='comment'),
    path('reply/<pk>/', RepCommentView.as_view(), name='comment'),
    path('upvote-comment/<pk>/', UpVoteComment.as_view(), name='upvote-comment/'),
    path('downvote-comment/<pk>/', DownVoteComment.as_view(), name='downvote-comment//'),

]
