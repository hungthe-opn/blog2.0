from django.urls import path
from .views import CategoryDetailView, CategoryView


app_name = 'category'

urlpatterns = [
    path('', CategoryView.as_view(), name='category_list'),
    path('<pk>/', CategoryDetailView.as_view(), name='category_detail'),
]