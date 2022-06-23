import secrets

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import UniqueConstraint, Q

from rest_framework.exceptions import NotAuthenticated

from core.user_files.models import UserFile

from .mixins import (
    OrderableMixin,
    PolymorphicContentTypeMixin,
    CreatedAndUpdatedOnMixin,
    TrashableModelMixin,
    ParentGroupTrashableModelMixin,
)
from .exceptions import UserNotInGroup, UserInvalidGroupPermissionsError

__all__ = [
    "Settings",
    "UserLogEntry",
    "UserFile",
]

User = get_user_model()

# The difference between an admin and member right now is that an admin has
# permissions to update, delete and manage the members of a group.
GROUP_USER_PERMISSION_ADMIN = "ADMIN"
GROUP_USER_PERMISSION_MEMBER = "MEMBER"
GROUP_USER_PERMISSION_CHOICES = (
    (GROUP_USER_PERMISSION_ADMIN, "Admin"),
    (GROUP_USER_PERMISSION_MEMBER, "Member"),
)


class Settings(models.Model):
    """
    The settings model represents the application wide settings that only admins can
    change. This table can only contain a single row.
    """

    instance_id = models.SlugField(default=secrets.token_urlsafe)
    allow_new_signups = models.BooleanField(
        default=True,
        help_text="Indicates whether new users can create a new account when signing "
                  "up.",
    )


class UserProfile(models.Model):
    """
    User profile to store user specific information that can't be stored in
    default user model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    language = models.TextField(
        max_length=10,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        help_text="An ISO 639 language code (with optional variant) "
                  "selected by the user. Ex: en-GB.",
    )


class UserLogEntry(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=(("SIGNED_IN", "Signed in"),))
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]
