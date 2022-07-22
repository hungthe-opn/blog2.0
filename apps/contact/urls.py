from django.urls import path

from apps.contact.views import ContactCreateView

app_name = 'contact'

urlpatterns = [
    path('', ContactCreateView.as_view())

]