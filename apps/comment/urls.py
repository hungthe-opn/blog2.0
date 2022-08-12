from django.urls import path

from .views import CommentBlog, RepComment,UpVoteComment,DownVoteComment, CountReplyPost

app_name = 'comments'

urlpatterns = [
    path('<pk>/', CommentBlog.as_view(), name='comment'),
    path('reply/<pk>/', RepComment.as_view(), name='comment'),
    path('count/<pk>/', CountReplyPost.as_view(), name='count'),
    path('upvote-comment/<pk>/', UpVoteComment.as_view(), name='upvote-comment/'),
    path('downvote-comment/<pk>/', DownVoteComment.as_view(), name='down-vote-comment//'),

]
