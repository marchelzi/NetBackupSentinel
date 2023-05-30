import re
from ndam.devices.base import BaseSSHDevice
from ndam.devices.exceptions import NoBackupData


class Mikrotik(BaseSSHDevice):
    def __init__(self, name, ip, username, password, port=22):
        super().__init__(name, ip, username, password, port)
        self.rsc_export_command = "/export"
        self.file = None
        self.backup_data = None

    def export(self):
        self._connect()
        result = self._execute(self.rsc_export_command)
        self._close()
        return self.strip_export(result)

    def strip_export(self, export):
        # remove line startwith #, use regex
        regex = r"^#.*\n"
        subst = ""
        result = re.sub(regex, subst, export, 0, re.MULTILINE)
        return result

    def is_same_config(self, export1, export2):
        return export1 == export2

    def is_same_config_with_diff(self, export1, export2):
        return self.compare(export1, export2) == ""

    def backup(self):
        export = self.export()
        self.backup_data = export
        return self.export()

    def to_file(self, export, filename=None):
        if self.backup_data is None:
            raise NoBackupData("No backup data found")
        if filename is None:
            filename = f"{self.ip}.rsc"

        with open(filename, "w") as f:
            f.write(export)
