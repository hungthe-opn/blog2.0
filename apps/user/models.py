from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.


class CusCustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_author', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_author') is not True:
            raise ValueError('Superuser = True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Staff = True... OK?')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('Need Email Oke?'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class RankModel(models.TextChoices):
    Lv1 = 'Thành viên mới'
    Lv2 = 'Người dùng'
    Lv3 = 'Người dùng nổi bật'
    Lv4 = 'Fan cứng'
    Lv5 = 'Người có tầm ảnh hưởng'
    Lv6 = 'Quản trị viên'


class CreateUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email add'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    rank = models.CharField(max_length=30, choices=RankModel.choices, default=RankModel.Lv1)
    is_admin = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = CusCustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name

