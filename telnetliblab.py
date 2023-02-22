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

tn.write(b"conf t\n")
sleep(1)
tn.write(b"int g0/1\n")
sleep(1)
tn.write(b"ip address 172.31.116.17 255.255.255.240\n")
sleep(2)
tn.write(b"no sh\n")
sleep(1)
tn.write(b"do sh ip int br\n")
sleep(2)
tn.write(b"do wr\n")
sleep(2)
for i in range(3):
    tn.write(b"exit\n")
    sleep(1)

output = tn.read_very_eager()
print(output.decode('ascii'))

tn.close()