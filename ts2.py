import sys
import socket as soc

class DNS:
    def __init__(self, host, ip, flag):
        self.host = host
        self.ip = ip
        self.flag = flag
    
    def toString(self):
        return "{} {} {}".format(self.host, self.ip, self.flag)
        
queries = []
def dns_table():
	try:
		file = open("PROJ2-DNSTS2.txt", "r")
		i = 0
		for tokens in file:
			strings = tokens.split()
			queries.append(DNS(strings[0], strings[1], strings[2])) 
			i += 1
	except soc.error as err:
		print("Error opening file: {}".format(err))
	print("[Ts2]: Dns table ready")
	file.close()

def tsServer(ts2ListenPort):
    try:
        ts2 = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        print("[Ts2]: Connection success with LS")
    except soc.error as err:
        print("[Ts2]: Error connecting to {}".format(err))
    
    ts2host = soc.gethostname()
    ts2_ip = soc.gethostbyname(ts2host)
    tServer_bind = ('', ts2ListenPort)
    
    ts2.bind(tServer_bind)
    ts2.listen(1)
    print("[Ts1]: Host: {}, IP: {}".format(ts2host, ts2_ip))
    
    def findhosts(tokens):
        for every in queries:
            if every.host.lower() == tokens.lower():
                return every.toString()
        return False
    
    while True:
        conn, addr = ts2.accept()
        ls_query = conn.recv(200).decode("utf-8")
        print("[Ts2]: {}".format(ls_query))
        
        dns_found = findhosts(ls_query)
    
        if dns_found == False:
            dns_found = "{} - Error:HOST NOT FOUND".format(ls_query)
        print("[Ts2]: {}".format(dns_found))
        conn.send(dns_found.encode("utf-8"))       
    ts2.close()

if __name__ == "__main__":
    dns_table()
    tsServer(int(sys.argv[1]))