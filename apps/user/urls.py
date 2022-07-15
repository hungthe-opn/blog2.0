from django.urls import path
from .views import CustomUserCreate, BlacklistTokenView, UpdateInformationView, UserInforView,UserDetailsView,UserFollowerView,UserFollow

app_name = 'users'
urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='create_user'),
    path('update/', UpdateInformationView.as_view(), name='update_user'),
    path('info/', UserInforView.as_view(), name='user_infor'),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
    path('follow/<pk>', UserFollowerView.as_view(), name='follow'),
    path('get-follow/', UserFollow.as_view(), name='list-follow'),
    path('get-user/<pk>', UserDetailsView.as_view(), name='list-follow'),

]
