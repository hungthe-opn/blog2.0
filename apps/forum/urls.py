from django.urls import path
from .views import AddBlogForum,ListBlogView,DetailForumView


app_name = 'forum'

urlpatterns = [
    path('', AddBlogForum.as_view(), name='add-post'),
    path('list-blog/', ListBlogView.as_view(), name='list-blog'),
    path('detail-forum/<pk>', DetailForumView.as_view(), name='list-blog'),

    # path('blog-admin/<pk>', UpdateBlogView.as_view(), name='admin-blog'),
    # path('user-role', UserRoleView.as_view(), name='user-role'),
    # path('delete-blog/<pk>', DeleteExportManageView.as_view(), name='delete'),
    # path('edit/<pk>', UpdateInsuranceView.as_view(), name='edit'),

]
