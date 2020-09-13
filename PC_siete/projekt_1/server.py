from socket import *
import subprocess , re
from time import sleep
import sys

try:
	port=int(sys.argv[1])
except ValueError as e:
	raise

serverPort = port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)

# Trieda pre výpočet vyťaženosti procesoru
class GetCpuLoad(object):


    def __init__(self, percentage=True, sleeptime = 1):
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
        cpu_infos = {}
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        start = self.getcputime()

        sleep(self.sleeptime)
        stop = self.getcputime()

        cpu_load = {}

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: CPU_Percentage})
        return cpu_load

# Začiatok smyčky
while 1:

	# Všetky možné hlavičky podla situácie ktorá nastane
    head = """HTTP/1.1 200 OK
Server: Python Socket
Contetnt-Type: text/plain
Connection: close

"""
    head2 = """HTTP/1.1 200 OK
Server: Python Socket
Contetnt-Type: application/json
Connection: close

"""

    head_ERR1 = """HTTP/1.1 406 Not Acceptable
Server: Python Socket
Connection: close

"""

    head_ERR2 = """HTTP/1.1 404 Not Found
Server: Python Socket
Connection: close

"""

    head_ERR3 = """HTTP/1.1 405 Method Not Allowed
Server: Python Socket
Connection: close

"""

    head_ERR4 = """HTTP/1.1 505 Version Not Supported
Server: Python Socket
Connection: close

"""


    clientSocket, clientAddress = serverSocket.accept()
    data = clientSocket.recv(1024)
    data2 = data.decode()
    
    tmp=0
    zaciatok = data2.find("Accept:")
    zaciatok = zaciatok+7
    json = 0
    koniec = data2.find("\n", zaciatok)

    # Zistenie čo je možné posielať tak že nahladnem čo je za Accept:
    if data2.find("application/json",zaciatok,koniec) >= 0:
    	head = head2
    	json = 1
    elif data2.find("text/plain",zaciatok,koniec) >= 0:
    	head = head
    elif data2.find("*/*",zaciatok,koniec) >= 0:
    	head = head
    else:
    	head = head_ERR1
    	clientSocket.send(head.encode())
    	clientSocket.close()
    	continue

    # Ak hlavička neobsahuje GET ale POST
    if data2.find("GET ") < 0:
    	head = head_ERR3
    	clientSocket.send(head.encode())
    	clientSocket.close()
    	continue

    # Ak je zlá verzia HTTP protokolu
    if data2.find("HTTP/1.1") < 0:
    	head = head_ERR4
    	clientSocket.send(head.encode())
    	clientSocket.close()
    	continue

    # Spracovanie požiadavku /hostname
    if data2.find("GET /hostname") >= 0:
        hostname = gethostname()
        if json == 1:
        	hostname = "{ \"hostname\" : \"%s\" }" % hostname
        head = head+hostname+"\n"

    # Spracovanie požiadavku /cpu-name
    elif data2.find("GET /cpu-name") >= 0:
        command = "cat /proc/cpuinfo"
        name = subprocess.check_output(command, shell=True).strip().decode()
        for line in name.split("\n"):
            if "model name" in line:
                name = re.sub( ".*model name.*:", "", line,1)
        if json == 1:
        	name = "{ \"cpu-name\" : \"%s\" }" % name
        head = head+ name+"\n"

    # Spracovanie požiadavku /load?refresh
    elif data2.find("GET /load?refresh=") >= 0:
    	index1 = data2.find("refresh=")+8
    	index2 = data2.find(" ",index1)
    	hed = "text/plain"
    	ref = (data2[index1:index2])
    	try:
    		ref = int(ref)
    	except ValueError as e:
    		raise

    	x=GetCpuLoad()
    	data3 = x.getcpuload()
    	for x in list(data3)[0:1]:
    		data4 = round((data3[x]),1)
    		data4= str(data4)+"%"
    	if json == 1:
        	data4 = "{ \"load?refresh\" : \"%s\" }" % data4
        	hed = "application/json"

    	head = """HTTP/1.1 200 OK
Server: Python Socket
Contetnt-Type: {}
Refresh: {}
Connection: close

""".format(hed, ref)

    	head = head+data4+"\n"
    	tmp = 1

    #Spracovanie požiadavku /load
    elif data2.find("GET /load") >= 0 and tmp == 0:
    	x=GetCpuLoad()
    	data3 = x.getcpuload()
    	for x in list(data3)[0:1]:
    		data4 = round((data3[x]),1)
    		data4 = str(data4)+"%"
    	if json == 1:
        	data4 = "{ \"load\" : \"%s\" }" % data4
    	head = head+data4+"\n"
    else:
    	head = head_ERR2
    	clientSocket.send(head.encode())
    	clientSocket.close()
    	continue

    # Odoslanie správy s hlavičkou a uzavretie socketu
    clientSocket.send(head.encode())
    clientSocket.close()