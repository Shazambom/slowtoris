import socket, sys, time, random, ssl, threading

class packetA(threading.Thread):
	def __init__(self, host, port, ssl):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.ssl = ssl
		self.startTime = 0
		self.endTime = 0

	def run(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			if self.ssl:
				s = ssl.wrap_socket(s)
			s.settimeout(15)
			self.startTime = time.time()
			s.connect((self.host, self.port))
			s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
			s.send(("Host: "+self.host+"\r\nUser-Agent: {}\r\n".format("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0")).encode("utf-8"))
			s.send(("{}\r\n".format("Accept-language: en-US,en,q=0.5")).encode("utf-8"))
			info = s.recv(4096)
		except Exception as err:
			print(err)
			self.endTime = time.time()
			return
	def getTime(self):
		return self.endTime - self.startTime

class packetB(threading.Thread):
	def __init__(self, host, port, ssl):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.ssl = ssl
		self.startTime = 0
		self.endTime = 0

	def run(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			if self.ssl:
				s = ssl.wrap_socket(s)
			s.settimeout(15)
			self.startTime = time.time()
			s.connect((self.host, self.port))
			s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
			s.send(("Host: "+self.host+"\r\nUser-Agent: {}\r\n".format("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36")).encode("utf-8"))
			s.send(("{}\r\n".format("Accept-language: en-US,en,q=0.5")).encode("utf-8"))
			time.sleep(10)
			s.send(("X-a: {}\r\n".format(random.randint(1, 5000))).encode("utf-8"))
			info = s.recv(4096)
		except Exception as err:
			print(err)
			self.endTime = time.time()
			return
	def getTime(self):
		return self.endTime - self.startTime


if __name__ == "__main__":
	args = sys.argv[1:]
	host = None
	port = 80
	ssl = False
	try:
		host = str(args[0])
		port = int(args[1])
		ssl = str(args[2]).lower == "y"
	except:
		print("Incorrect args format")
		print("Correct args format: python3 slowlorisprobe.py IPv4(str) port(int) isHTTPS(Y/N)")
		exit(1)
	first = packetA(host, port, ssl)
	second = packetB(host, port, ssl)
	print("Sending first payload")
	first.start()
	print("Sending second payload")
	second.start()
	first.join()
	print("First payload executed")
	second.join()
	print("Second payload executed")
	firstTimeoutTime = first.getTime()
	print("First payload timeout time: " + str(firstTimeoutTime))
	secondTimeoutTime = second.getTime()
	print("Second payload timeout time: " + str(secondTimeoutTime))
	if secondTimeoutTime - firstTimeoutTime >= 10:
		print(host+":"+str(port)+" is likely vulnerable to Slowloris attack")
	else:
		print(host+":"+str(port)+" not vulnerable to Slowloris attack")



