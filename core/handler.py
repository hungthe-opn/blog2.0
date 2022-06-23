from django.contrib.auth import get_user_model

from .models import (
    Settings,
)
from .exceptions import (
    IsNotAdminError,
)
from .utils import set_allowed_attrs

User = get_user_model()


class CoreHandler:
    def get_settings(self):
        """
        Returns a settings model instance containing all the admin configured settings.

        :return: The settings instance.
        :rtype: Settings
        """

        try:
            return Settings.objects.all()[:1].get()
        except Settings.DoesNotExist:
            return Settings.objects.create()

    def update_settings(self, user, settings_instance=None, **kwargs):
        """
        Updates one or more setting values if the user has staff permissions.

        :param user: The user on whose behalf the settings are updated.
        :type user: User
        :param settings_instance: If already fetched, the settings instance can be
            provided to avoid fetching the values for a second time.
        :type settings_instance: Settings
        :param kwargs: An dict containing the settings that need to be updated.
        :type kwargs: dict
        :return: The update settings instance.
        :rtype: Settings
        """

        if not user.is_staff:
            raise IsNotAdminError(user)

        if not settings_instance:
            settings_instance = self.get_settings()

        settings_instance = set_allowed_attrs(
            kwargs, ["allow_new_signups"], settings_instance
        )

        settings_instance.save()
        return settings_instance
