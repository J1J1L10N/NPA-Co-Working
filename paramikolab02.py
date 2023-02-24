from time import sleep
from paramiko import SSHClient, AutoAddPolicy, Channel
from os import path

devices_ip = ["172.31.116.4", "172.31.116.5", "172.31.116.6"]

class NoiceParamiko:
    def __init__(self) -> None:
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    def send_command(ssh: Channel, command: str) -> None:
        ssh.send(f"{command}\n")
        sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

    def execute(self, ip: str) -> None:
        self.client.connect(hostname=ip, username="admin", key_filename=path.join(path.expanduser('~'), ".ssh", "id_rsa"))
        print(f"Connecting to... {ip}")
        with self.client.invoke_shell() as ssh:
            print(f"Connected to {ip}")

            self.send_command(ssh, "terminal length 0")
            self.send_command(ssh, "sh ip int br")

if __name__ == '__main__':
    client = NoiceParamiko()
    client.execute(devices_ip[0])
