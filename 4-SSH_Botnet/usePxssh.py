from pexpect import pxssh

def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print(s.before)

def connect(host, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except:
        print('[-] Error Connecting')
        exit(0)
host = '192.168.249.128'
user = 'root'
password='toor'
s= connect(host,user,password)
send_command(s, 'cat /etc/shadow | grep root')