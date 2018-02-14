import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)		#设置信号量

def connScan(targetHost, targetPort):
	try:
		connSocket = socket(AF_INET, SOCK_STREAM)
		connSocket.connect((targetHost, targetPort))
		connSocket.send("Test-Open\r\n".encode('utf-8'))
		result = connSocket.recv(512)
		screenLock.acquire()
		print("[+] %d/tcp open" %targetPort+"\n")
		# print("[+] "+str(result)+"\n")	#打印服务Banner
	except:
		screenLock.acquire()
		print("[-] %d/tcp closed" %targetPort+"\n")
	finally:
		screenLock.release()
		connSocket.close()

def portScan(targetHost, targetPorts):
	try:
		targetIP = gethostbyname(targetHost)
	except:
		print("[-] Cannot resolve '%s': Unknown host." %targetHost+"\n")
		return
	try:
		targetName = gethostbyaddr(targetIP)
		print("\n[+] Scanning "+targetName[0]+"\n")		#因为gethostbyaddr()返回
	except:												#的是三元组
		print("\n[+] Scanning "+targetIP+"\n")
	setdefaulttimeout(1)
	for targetPort in targetPorts:
		t = Thread(target=connScan, args=(targetHost, int(targetPort)))
		t.start()

def main():
	parser = optparse.OptionParser("usage %prog "+\
		"-H <target host> -p <target port(s)>")
	parser.add_option('-H', dest='targetHost', type='string', \
		help='specify target host')
	parser.add_option('-p', dest='targetPorts', type='string', \
		help='specify target port(s) separated by comma')
	(options, args) = parser.parse_args()
	targetHost = options.targetHost
	targetPorts = str(options.targetPorts).split(',')
	if (targetHost == None) | (targetPorts == None):
		print(parser.usage)
		exit(0)
	portScan(targetHost, targetPorts)

if __name__ == '__main__':
	main()
