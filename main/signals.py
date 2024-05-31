from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
import json
from .consumers import send_notification

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        send_notification(instance.sender, instance.receiver, instance.content)
