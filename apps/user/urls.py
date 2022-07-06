from django.urls import path
from .views import CustomUserCreate, BlacklistTokenView, UpdateInformationView, UserInforView

app_name = 'users'
urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='create_user'),
    path('update/', UpdateInformationView.as_view(), name='update_user'),
    path('info/', UserInforView.as_view(), name='user_infor'),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
]
