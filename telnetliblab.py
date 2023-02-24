from getpass import getpass
from telnetlib import Telnet
from time import sleep

host = "172.31.116.4"

def login(tn, credential):
    tn.read_until(credential.encode('ascii') + b":")
    usercred = input("Enter username: ") if credential == "Username" else getpass()
    tn.write(usercred.encode('ascii') + b"\n")
    sleep(1)

def setint(tn):
    Setupcmd = ["conf t", "int g0/1", "ip address 172.31.116.17 255.255.255.240"
            , "no sh", "do sh ip int br", "do wr", "exit", "exit", "exit"]
    for cmd in Setupcmd:
        tn.write((cmd + '\n').encode('ascii'))
        sleep(2)
    output = tn.read_very_eager()
    print(output.decode('ascii'))

def main():
    tn = Telnet(host, 23, 5)
    login(tn, "Username")
    login(tn, "Password")
    setint(tn)
    tn.close()

if __name__ == "__main__":
    main()