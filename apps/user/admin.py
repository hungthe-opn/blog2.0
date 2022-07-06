from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django.db import models
from .models import CreateUserModel


# Register your models here.


class UserAdminConfig(UserAdmin):
    model = CreateUserModel
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff', 'is_author',)
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff', 'is_author', 'is_report', 'rank','image')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'rank',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_author', 'is_report',)}),
        ('Personal', {'fields': ('about','image')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_report')}
         ),
    )


admin.site.register(CreateUserModel, UserAdminConfig)
