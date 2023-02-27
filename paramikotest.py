from time import sleep
from paramiko import SSHClient, AutoAddPolicy, Channel, Transport
from os import path

devices_ip = ["172.31.116.4", "172.31.116.5", "172.31.116.6"]

class NoiceParamiko:
    def __init__(self) -> None:
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    def send_command(self, ssh: Channel, command: str) -> None:
        ssh.send(f"{command}\n")
        sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

    def execute(self, ip: str) -> None:
        print(f"Connecting to... {ip}")
        self.client.connect(ip, username="admin", key_filename="id_rsa", disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
        print(f"Connected to {ip}")

        with self.client.invoke_shell() as ssh:
            self.send_command(ssh, "terminal length 0")
            self.send_command(ssh, "sh ip int br")

if __name__ == '__main__':
    client = NoiceParamiko()
    [client.execute(ip) for ip in devices_ip]
