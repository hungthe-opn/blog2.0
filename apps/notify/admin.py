from django.contrib import admin

# Register your models here.

from apps.notify.models import NotificationModel

admin.site.register(NotificationModel)