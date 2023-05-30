import paramiko
import difflib
import logging

logger = logging.getLogger(__name__)


class BaseDevice:
    def __init__(self, name, ip, username, password, port):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

    def compare(self, export1, export2, filename_1="export1", filename_2="export2"):
        diff = difflib.unified_diff(
            export1.splitlines(keepends=True),
            export2.splitlines(keepends=True),
            fromfile=filename_1,
            tofile=filename_2,
        )

        # show only lines that start with + or -
        diff = [line for line in diff if line.startswith("+") or line.startswith("-")]
        return "".join(diff)


class BaseSSHDevice(BaseDevice):
    def __init__(self, name, ip, username, password, port, *args, **kwargs):
        super().__init__(name, ip, username, password, port)

        self.allow_agent = kwargs.get("allow_agent", False)
        self.look_for_keys = kwargs.get("look_for_keys", False)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def _connect(self):
        logging.info(f"Connecting to {self.ip}")

        self.client.connect(
            self.ip,
            self.port,
            self.username,
            self.password,
            allow_agent=self.allow_agent,
            look_for_keys=self.look_for_keys,
        )

        logging.info(f"Connected to {self.ip}")

    def _close(self):
        logging.info(f"Closing connection to {self.ip}")
        self.client.close()

    def _execute(self, command):
        logging.info(f"Executing command {command}")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def _execute_with_sudo(self, command):
        logging.info(f"Executing command {command} with sudo")
        stdin, stdout, stderr = self.client.exec_command(f"sudo {command}")
        stdin.write(f"{self.password}\n")
        stdin.flush()
        return stdout.read().decode()

    def _execute_with_sudo_without_password(self, command):
        logging.info(f"Executing command {command} with sudo without password")
        stdin, stdout, stderr = self.client.exec_command(f"sudo {command}")
        return stdout.read().decode()

    def test_connection(self):
        try:
            self._connect()
            self._close()
            return True
        except Exception as e:
            logging.error(f"Failed to connect to {self.ip}")
            logging.error(e)
            return False
