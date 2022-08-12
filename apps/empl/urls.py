from django.urls import path
from .views import AddBlog, UpdateBlog, UserRole, DeleteExport, UpdateInsurance

app_name = 'empl'

urlpatterns = [
    path('', AddBlog.as_view(), name='add-post'),
    path('blog-admin/<pk>', UpdateBlog.as_view(), name='admin-blog'),
    path('user-role', UserRole.as_view(), name='user-role'),
    path('delete-blog/<pk>', DeleteExport.as_view(), name='delete'),
    path('edit/<pk>', UpdateInsurance.as_view(), name='edit'),

]
