from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from api import constant
from apps.blog_it.models import BaseModel


# Create your models here.


class UserGroupModel(BaseModel):
    name = models.CharField(blank=True, null=True, max_length=254)
    queue_id = models.CharField(blank=True, null=True, max_length=254)
    is_default = models.BooleanField(default=False, null=True, blank=True)
    caller_phone_number = models.CharField(blank=True, null=True, max_length=32)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'tbl_user_group'
        ordering = ['id']


class CusCustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_author', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_report', False)

        if other_fields.get('is_author') is not True:
            raise ValueError('Superuser = True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Staff = True... OK?')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('Err'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CreateUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email add'), max_length=254)
    user_name = models.CharField(max_length=150, null=True, default=constant.USER_RANK_Lv1)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    rank = models.CharField(max_length=30, choices=constant.USER_RANK_OPTION, default=constant.USER_RANK_Lv1)
    image = models.ImageField(_('image'), max_length=100, null=True, blank=True)
    home = models.CharField(max_length=256, null=True)
    is_admin = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_report = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    is_employee = models.BooleanField(blank=False, null=False, default=False)
    sex = models.CharField(max_length=30, choices=constant.USER_SEX_OPTION, default=constant.USER_SEX_NEW)
    groups = models.ManyToManyField(UserGroupModel, related_name='users', through='UserGroupRelation')
    objects = CusCustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    class Meta:
        db_table = 'tbl_user'
        ordering = ['id']
        unique_together = ('email',)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(CreateUserModel, self).save(*args, **kwargs)
        self.name = str(self.rank.encode('unicode_escape'))


class UserGroupRelation(models.Model):
    user = models.ForeignKey(CreateUserModel, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroupModel, on_delete=models.CASCADE)
    date_joined = models.DateField()

    class Meta:
        db_table = 'tbl_user_group_relationship'
        unique_together = ['user', 'group']


class Follow(models.Model):
    from_user = models.ForeignKey("CreateUserModel", related_name='followings', on_delete=models.CASCADE)
    to_user = models.ForeignKey("CreateUserModel", related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    muted = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('from_user', 'to_user')
        db_table = 'tbl_user_follow'

    def __str__(self) -> str:
        return f"{self.from_user.user_name} started following {self.to_user.user_name}"
