import uuid
from django.db import models
from django.conf import settings
from ndam.devices.mikrotik import Mikrotik
from django_cryptography.fields import encrypt

SECRET_KEY = settings.SECRET_KEY


# Create your models here.


class DeviceCredential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = encrypt(models.CharField(max_length=100))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Device Credential"
        verbose_name_plural = "Device Credentials"


class Device(models.Model):
    _CONNECTION_TYPE = ((0, "SSH"),)
    _DEVICE_MODUL = ((0, "Mikrotik"),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField("IP Address")
    port = models.IntegerField(default=22)
    connection_type = models.IntegerField(choices=_CONNECTION_TYPE, default=0)
    modul_type = models.IntegerField(choices=_DEVICE_MODUL, default=0)
    credential = models.ForeignKey(
        DeviceCredential,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
    )
    enabled = models.BooleanField(
        default=True, help_text="Enable or disable device backup"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._modul = None

    def get_modul(self):
        match self.modul_type:
            case 0:
                return Mikrotik
        raise ValueError("Modul not found")

    def init_modul(self):
        modul = self.get_modul()
        # check if model is initialized from database
        if self.pk is not None and self.credential is not None:
            return modul(
                self.name,
                self.ip_address,
                self.credential.username,
                self.credential.password,
                self.port,
            )
        return None

    @property
    def modul(self):
        if self._modul is None:
            self._modul = self.init_modul()
        return self._modul


class DeviceBackup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(
        Device, on_delete=models.SET_NULL, related_name="backups", null=True, blank=True
    )
    description = models.TextField()
    data = models.FileField(upload_to="backups")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class DeviceStatus(models.Model):
    _BACKUP_STATE = ((0, "Success"), (1, "Failed"), (2, "In Progress"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="status", null=True, blank=True
    )
    last_backup = models.DateTimeField(null=True, blank=True, editable=False)
    state = models.IntegerField(choices=_BACKUP_STATE, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Device Status"
        verbose_name_plural = "Device Status"
        ordering = ["-created_at"]
