import pexpect

PROMPT = '#'
Devices_ip = ['172.31.116.4', '172.31.116.5', '172.31.116.6']
Username = "admin"
Password = "cisco"

def setloopback(ip, iploopback):
    Command = ["conf t", "interface loopback 0", f"ip address {iploopback} 255.255.255.255"]
    Checkpoint = ["exit", "exit", "sh ip int br", "exit"]
    child = pexpect.spawn('telnet ' + ip)
    child.expect('Username')
    child.sendline(Username)
    child.expect('Password')
    child.senline(Password)
    child.expect(PROMPT)
    for cmd in Command: child.sendline(cmd)
    child.sendline("exit") #exit from loopback interface
    child.sendline("exit") #exit from priviledge mode
    child.expect(PROMPT)
    child.sendline("sh ip int br")
    child.expect(PROMPT)
    result = child.before
    print(result.decode('UTF-8'))
    child.sendline("exit") #exit from session
    

def main():
    for i, ip in enumerate(Devices_ip):
        iploopback = ".".join([str(i + 1)] * 4)
        setloopback(ip, iploopback)
main()