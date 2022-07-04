from django.urls import path
from .views import AddBlogView, UpdateBlogView

app_name = 'empl'

urlpatterns = [
    path('', AddBlogView.as_view(), name='add-post'),
    path('blog-admin/<pk>', UpdateBlogView.as_view(), name='admin-blog'),

]
