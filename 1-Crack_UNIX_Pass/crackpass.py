import crypt

def testPass(cryptPass):
	salt = cryptPass[0:2]
	dictFile = open('dictionary.txt', 'r')
	for word in dictFile.readlines():
		word = word.strip('\n')
		cryptWord = crypt.crypt(word, salt)
		if (cryptWord == cryptPass):
			print("[+] Crack Succeeded! The Password Is: " + word + "\n")
			return
	print("[-] Crack Failed! \n")
	return

def main():
	passFile = open('password.txt')
	for record in passFile.readlines():
		if ":" in record:
			user = record.split(':')[0]
			cryptPass = record.split(':')[1].strip('\n')
			print("[*] Cracking Password For: " + user)
			testPass(cryptPass)

if __name__ == "__main__":
	main()
