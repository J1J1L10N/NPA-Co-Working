from time import sleep
from paramiko import SSHClient, AutoAddPolicy, Channel, Transport
from os import path

USERNAME = "admin"
PASSWORD = "cisco"

routers = [1, 2, 3]
devices_ip = "172.31.116.%s"

command = {
    "r1": ["conf t", \
            "ip access-list extended Block-telnet/SSH", "deny tcp any any eq 22", "deny tcp any any eq 23", "permit ip any any", \
            "int g0/1", "ip add 172.31.116.17 255.255.255.240", "no shut", "ip access-group Block-telnet/SSH in", \
            "int g0/2", "ip add 172.31.116.34 255.255.255.240", "no shut", "ip access-group Block-telnet/SSH in", "exit", \
            "router ospf 1 vrf control-data", "router-id 1.1.1.1", "network 1.1.1.1 0.0.0.0 area 0", \
            "network 172.31.116.16 0.0.0.15 area 0", "network 172.31.116.32 0.0.0.15 area 0", "do wr"],
    "r2": ["conf t", \
            "ip access-list extended Block-telnet/SSH", "deny tcp any any eq 22", "deny tcp any any eq 23", "permit ip any any", \
            "int g0/1", "ip add 172.31.116.33 255.255.255.240", "no shut", "ip access-group Block-telnet/SSH in", \
            "int g0/2", "ip add 172.31.116.50 255.255.255.240", "no shut", "ip access-group Block-telnet/SSH in", "exit", \
            "router ospf 1 vrf control-data", "router-id 2.2.2.2", "network 2.2.2.2 0.0.0.0 area 0", \
            "network 172.31.116.32 0.0.0.15 area 0", "network 172.31.116.48 0.0.0.15 area 0", "do wr"],
    "r3": ["conf t", \
            "ip access-list extended Block-telnet/SSH", "deny tcp any any eq 22", "deny tcp any any eq 23", "permit ip any any", \
            "int g0/1", "ip add 172.31.116.49 255.255.255.240", "no shut", "ip access-group Block-telnet/SSH in", \
            "int g0/2", "ip add dhcp", "no shut", "ip access-group Block-telnet/SSH in", "exit", \
            "ip route 0.0.0.0 0.0.0.0 192.168.122.1", \
            "router ospf 1 vrf control-data", "router-id 3.3.3.3", "default-information originate", \
            "network 3.3.3.3 0.0.0.0 area 0", "network 172.31.116.48 0.0.0.15 area 0", "exit", \
            "access-list 1 permit any", "ip nat inside source list 1 int g0/2 vrf control-data overload", \
            "int g0/1", "ip nat inside", "exit", "int g0/2", "ip nat outside", "exit", "do wr"] }


for r in routers:
    ip = devices_ip %(r + 3)
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username="admin", key_filename="id_rsa", disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})

    with client.invoke_shell() as ssh:
        print("Connecting to {} ...".format(ip))
        for i in command["r%s" %r]:
            ssh.send(i+ "\n")
            sleep(1)
            result = ssh.recv(1000).decode("ascii")
            print(result)
    client.close()