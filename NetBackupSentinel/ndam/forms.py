from django import forms
from ndam.models import Device, DeviceCredential


class DeviceCredentialForm(forms.ModelForm):
    class Meta:
        model = DeviceCredential
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(),
        }
        help_texts = {
            "name": "Credential Name",
            "username": "Credential Username",
            "password": "Credential Password",
        }


class DeviceForm(forms.ModelForm):
    credential = DeviceCredentialForm()
    test_connection = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Test device connection",
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = Device
        fields = "__all__"
        help_texts = {
            "name": "Hostname or Device Name",
            "ip_address": "Device IP Address",
            "port": "Device Port",
            "connection_type": "Connection Type",
            "modul_type": "Device Modul",
            "credential": "Device Credential",
            "enabled": "Enable or disable device backup",
        }
