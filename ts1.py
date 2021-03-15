import sys
import socket as soc

queries = []
def dns_table():
	try:
		file = open("PROJ2-DNSTS1.txt", "r")
		i = 0
		for tokens in file:
			strings = tokens.split()
			queries.append(DNS(strings[0], strings[1], strings[2])) 
			i += 1
	except soc.error as err:
		print("Error opening file: {}".format(err))
	print("[TS]: Dns table ready")
	file.close()

class DNS:
    def __init__(self, host, ip, flag):
        self.host = host
        self.ip = ip
        self.flag = flag
    
    def toString(self):
        return "{} {} {}".format(self.host, self.ip, self.flag)

def tsServer(ts1ListenPort):
    try:
        ts1 = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        print("[Ts1]: Connection success with LS")
    except soc.error as err:
        print("[Ts1]: Error connecting to {}".format(err))
    
    ts1host = soc.gethostname()
    ts1_ip = soc.gethostbyname(ts1host)
    tServer_bind = ('', ts1ListenPort)
    
    ts1.bind(tServer_bind)
    ts1.listen(1)
    print("[Ts1]: Host: {}, IP: {}".format(ts1host, ts1_ip))
    print("[Ts1]: Listening on {}".format(ts1ListenPort))
    
    def findhosts(tokens):
        for check in queries:
            if check.host.lower() == tokens.lower():
                return check.toString()
        return False
    
    while True:
        conn, addr = ts1.accept()
        ls_query = conn.recv(200).decode("utf-8")
        print("[Ts1]: {}".format(ls_query))
        
        dns_found = findhosts(ls_query)
    
        if dns_found == False:
            dns_found = "{} - Error:HOST NOT FOUND".format(ls_query)
        print("[Ts1]: {}".format(dns_found))
        conn.send(dns_found.encode("utf-8")) 
    ts1.close()

if __name__ == "__main__":
    dns_table()
    tsServer(int(sys.argv[1]))