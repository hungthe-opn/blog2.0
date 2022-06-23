from django.db import transaction
from django.dispatch import receiver

from core import signals
from .tasks import broadcast_to_group, broadcast_to_users


@receiver(signals.group_deleted)
def group_deleted(sender, group_id, group, group_users, user=None, **kwargs):
    transaction.on_commit(
        lambda: broadcast_to_users.delay(
            [u.id for u in group_users],
            {"type": "group_deleted", "group_id": group_id},
            getattr(user, "web_socket_id", None),
        )
    )


@receiver(signals.group_user_deleted)
def group_user_deleted(sender, group_user, user, **kwargs):
    transaction.on_commit(
        lambda: broadcast_to_users.delay(
            [group_user.user_id],
            {"type": "group_deleted", "group_id": group_user.group_id},
            getattr(user, "web_socket_id", None),
        )
    )


@receiver(signals.application_deleted)
def application_deleted(sender, application_id, application, user, **kwargs):
    transaction.on_commit(
        lambda: broadcast_to_group.delay(
            application.group_id,
            {"type": "application_deleted", "application_id": application_id},
            getattr(user, "web_socket_id", None),
        )
    )


@receiver(signals.applications_reordered)
def applications_reordered(sender, group, order, user, **kwargs):
    transaction.on_commit(
        lambda: broadcast_to_group.delay(
            group.id,
            {
                "type": "applications_reordered",
                "group_id": group.id,
                "order": order,
            },
            getattr(user, "web_socket_id", None),
        )
    )
