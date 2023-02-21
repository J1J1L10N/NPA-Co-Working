import pexpect

PROMPT = '#'
Devices_ip = ['172.31.116.4', '172.31.116.5', '172.31.116.6']
Username = "admin"
Password = "cisco"

def setloopback(ip, iploopback):
    Command = ["conf t", "interface loopback 0", f"ip address {iploopback} 255.255.255.255"]
    child = pexpect.spawn(f'telnet {ip}')
    print('Authenticating...')
    child.expect('Username')
    child.sendline(Username)
    child.expect('Password')
    child.sendline(Password)

    print('Enabling...')
    child.expect(PROMPT)
    for cmd in Command:
        print(f'-> Running "{cmd}"')
        child.sendline(cmd)
        child.expect(PROMPT)
    child.sendline("exit") # exit from loopback interface
    child.expect(PROMPT)
    child.sendline("exit") # exit from config terminal
    child.expect(PROMPT)

    print('Generating Result...')
    child.sendline("show ip interface brief")
    child.expect(PROMPT)
    result = child.before
    print('-'*20)
    print(result.decode('UTF-8')) #show result
    print('-'*20)
    child.sendline("wr") #save config
    child.sendline("exit") #exit from session
    print('Done!')

if __name__ == '__main__':
    for i, ip in enumerate(Devices_ip):
        iploopback = ".".join([str(i + 1)] * 4)
        print(f'setting on {ip} with loopback {iploopback}')
        setloopback(ip, iploopback)
