from django.urls import path

from .views import AddBlogForum, \
    ListBlogView, \
    DetailForumView, \
    ListBlogUserView, \
    InforUser, \
    DownvoteView, \
    UpvoteView, \
    ListForumFollowersView, ListBlogViewCount, \
    BookmarksPostView,\
ListBookmarksPostView

app_name = 'forum'

urlpatterns = [
    path('', AddBlogForum.as_view(), name='add-post'),
    path('list-view-count/', ListBlogViewCount.as_view(), name='view-count'),
    path('list-blog/', ListBlogView.as_view(), name='list-blog'),
    path('detail-forum/<pk>', DetailForumView.as_view(), name='detail-forum/'),
    path('user-blog/', ListBlogUserView.as_view(), name='user-blog'),
    path('account-blog/<pk>', InforUser.as_view(), name='account-blog/'),
    path('upvote-forum/<pk>', UpvoteView.as_view(), name='upvote'),
    path('downvote-forum/<pk>', DownvoteView.as_view(), name='down-vote'),
    path('list-followers/', ListForumFollowersView.as_view(), name='followers'),
    path('post-bookmark/<pk>', BookmarksPostView.as_view(), name='post-bookmark'),
    path('user-get-bookmark/', ListBookmarksPostView.as_view(), name='post-user-bookmarks'),

]
