from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptedField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encryptor = self.init_encryptor()

    def init_encryptor(self):
        SECRET_KEY = getattr(settings, "SECRET_KEY", None)
        SALT_KEY = getattr(settings, "SALT_KEY", None)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT_KEY.encode(),
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(SECRET_KEY.encode()))

        return Fernet(key)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self._decrypt(value)

    def to_python(self, value):
        if value is None:
            return value
        return self._decrypt(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return self._encrypt(value)

    def _encrypt(self, value):
        return self.encryptor.encrypt(value.encode()).decode()

    def _decrypt(self, value):
        return self.encryptor.decrypt(value.encode()).decode()
