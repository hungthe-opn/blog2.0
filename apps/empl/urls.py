from django.urls import path
from .views import AddBlogView, UpdateBlogView,UserRoleView

app_name = 'empl'

urlpatterns = [
    path('', AddBlogView.as_view(), name='add-post'),
    path('blog-admin/<pk>', UpdateBlogView.as_view(), name='admin-blog'),
    path('user-roleuser-role', UserRoleView.as_view(), name='user-role'),

]
