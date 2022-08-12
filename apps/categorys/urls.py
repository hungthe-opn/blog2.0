from django.urls import path
from .views import CategoryDetail, Category


app_name = 'category'

urlpatterns = [
    path('', Category.as_view(), name='category_list'),
    path('<pk>/', CategoryDetail.as_view(), name='category_detail'),
]