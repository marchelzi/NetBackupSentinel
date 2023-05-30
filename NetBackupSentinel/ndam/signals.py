from django.db.models.signals import post_save
from ndam.models import Device, DeviceStatus
from django.dispatch import receiver


@receiver(post_save, sender=Device)
def create_device_status(sender, instance, created, **kwargs):
    if created:
        DeviceStatus.objects.create(device=instance)
