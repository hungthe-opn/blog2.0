from django.urls import path
from .views import CustomUserCreate, BlacklistToken, UpdateInformation, UserInfor,UserDetail,UserFollower,UserFollows

app_name = 'users'
urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='create_user'),
    path('update/', UpdateInformation.as_view(), name='update_user'),
    path('info/', UserInfor.as_view(), name='user_infor'),
    path('logout/blacklist/', BlacklistToken.as_view(), name='blacklist'),
    path('follow/<pk>', UserFollower.as_view(), name='follow'),
    path('get-follow/', UserFollows.as_view(), name='list-follow'),
    path('get-user/<pk>', UserDetail.as_view(), name='list-follow'),

]
