from django.urls import path

from .views import AddBlogForum, \
    Posts, \
    DetailForum, \
    ListBlogUser, \
    InforUser, \
    DownVote, \
    Upvote, \
    ListForumFollowers, ViewCount, \
    BookmarksPosts, \
    ListBookmarksPosts, \
    EditPost

app_name = 'forum'

urlpatterns = [
    path('', AddBlogForum.as_view(), name='add-post'),
    path('list-view-count/', ViewCount.as_view(), name='view-count'),
    path('list-blog/', Posts.as_view(), name='list-blogs-forum'),
    path('detail-forum/<pk>', DetailForum.as_view(), name='detail-forum'),
    path('edit-forum/<pk>', EditPost.as_view(), name='edit-forum'),
    path('user-blog/', ListBlogUser.as_view(), name='user-blog'),
    path('account-blog/<pk>', InforUser.as_view(), name='account-blog/'),
    path('upvote-forum/<pk>', Upvote.as_view(), name='upvote'),
    path('downvote-forum/<pk>', DownVote.as_view(), name='down-vote'),
    path('list-followers/', ListForumFollowers.as_view(), name='followers'),
    path('post-bookmark/<pk>', BookmarksPosts.as_view(), name='post-bookmark'),
    path('user-get-bookmark/', ListBookmarksPosts.as_view(), name='post-user-bookmarks'),

]
