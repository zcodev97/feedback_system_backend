# # myapp/signals.py
# import logging
#
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from mms_api.models import LogEntry
#
# logger = logging.getLogger(__name__)
#
# @receiver(post_save, sender=User)
# def user_saved(sender, instance, **kwargs):
#     LogEntry.objects.create(
#         user=instance,
#         action='User saved',
#         details=f"User {instance.username} ({instance.id}) was saved.",
#     )
#
#
# @receiver(post_delete, sender=User)
# def user_deleted(sender, instance, **kwargs):
#     LogEntry.objects.create(
#         user=None,
#         action='User deleted',
#         details=f"User {instance.username} ({instance.id}) was deleted.",
#     )
#
# # You can define similar signal receivers for other models and actions you want to log.
