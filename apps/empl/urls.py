from django.urls import path
from .views import AddBlogView, UpdateBlogView, UserRoleView, DeleteExportManageView, UpdateInsuranceView

app_name = 'empl'

urlpatterns = [
    path('', AddBlogView.as_view(), name='add-post'),
    path('blog-admin/<pk>', UpdateBlogView.as_view(), name='admin-blog'),
    path('user-role', UserRoleView.as_view(), name='user-role'),
    path('delete-blog/<pk>', DeleteExportManageView.as_view(), name='delete'),
    path('edit/<pk>', UpdateInsuranceView.as_view(), name='edit'),

]
