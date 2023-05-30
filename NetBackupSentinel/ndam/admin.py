from django.contrib import admin
from ndam.models import Device, DeviceCredential, DeviceBackup


# Register your models here.
class DeviceCredentialAdmin(admin.ModelAdmin):
    list_display = ("name", "username")

    # for password form field


class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ip_address",
        "port",
        "connection_type",
        "modul_type",
        "credential",
        "created_at",
        "updated_at",
    )


class DeviceBackupAdmin(admin.ModelAdmin):
    list_display = ("device", "description", "data", "created_at")


admin.site.register(DeviceCredential, DeviceCredentialAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceBackup, DeviceBackupAdmin)
