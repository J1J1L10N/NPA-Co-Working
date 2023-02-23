from getpass import getpass
from telnetlib import Telnet
from time import sleep

host = "172.31.116.4"
user = input("Enter username: ")
password = getpass()

tn = Telnet(host, 23, 5)

tn.read_until(b"Username:")
tn.write(user.encode('ascii') + b"\n")
sleep(1)

tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n")
sleep(1)

Setupcmd = ["conf t", "int g0/1", "ip address 172.31.116.17 255.255.255.240"
        , "no sh", "do sh ip int br", "do wr", "exit", "exit", "exit"]
for cmd in Setupcmd:
    tn.write((cmd + '\n').encode('ascii'))
    sleep(2)

output = tn.read_very_eager()
print(output.decode('ascii'))

tn.close()