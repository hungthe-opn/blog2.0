from django.urls import path
from .views import AddBlogForum,ListBlogView,DetailForumView,ListBlogUserView,InforUser,DownvoteView,UpvoteView


app_name = 'forum'

urlpatterns = [
    path('', AddBlogForum.as_view(), name='add-post'),
    path('list-blog/', ListBlogView.as_view(), name='list-blog'),
    path('detail-forum/<pk>', DetailForumView.as_view(), name='list-blog'),
    path('user-blog/', ListBlogUserView.as_view(), name='user-blog'),
    path('account-blog/<pk>', InforUser.as_view(), name='user-blog'),
    path('upvote-forum/<pk>', UpvoteView.as_view(), name='upvote'),
    path('downvote-forum/<pk>', DownvoteView.as_view(), name='down-vote'),

    # path('blog-admin/<pk>', UpdateBlogView.as_view(), name='admin-blog'),
    # path('user-role', UserRoleView.as_view(), name='user-role'),
    # path('delete-blog/<pk>', DeleteExportManageView.as_view(), name='delete'),
    # path('edit/<pk>', UpdateInsuranceView.as_view(), name='edit'),

]
