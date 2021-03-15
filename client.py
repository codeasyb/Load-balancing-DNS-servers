import sys
import socket as soc
import time, random

def client(ls_host, ls_port):
    try: 
        sc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        print("[C]: Client has made connection")
    except soc.error as err:
        print("[C]: Error connecting to {}".format(err))
        
    # client will talk with Localhost
    sc_ip = soc.gethostbyname(ls_host)
    sc_servebind = ((sc_ip, ls_port))
    sc.connect(sc_servebind)
    print("[C]: Host: {}, Port: {}".format(ls_host, ls_port))
    print("[C]: Client made contact on port {}".format(ls_port))
    
    fp = open("PROJ2-HNS.txt", "r")
    fw = open('RESOLVED.txt', 'w')
    
    for line in fp:
        print("[C]: Sending {}".format(line.rstrip()))
        sc.send(line.rstrip().encode("utf-8"))
        time.sleep(random.random()*5)
        LS_response = sc.recv(256).decode("utf-8")
        ls_response_check = LS_response.split()
        # print("[Checking]: {}".format(LS_response))
        if len(ls_response_check) <= 3 and LS_response != ".":
            if ls_response_check[2] == 'A':
                # print("====> {}".format(LS_response))
                print("[LS]: {}".format(LS_response))
                fw.write(LS_response + '\n')
        else:
            fw.write(line.rstrip() + " - ERROR:HOST NOT FOUND\n")

    fp.close()
    fw.close()
    sc.close()
    exit()

if __name__ == '__main__':
    client(sys.argv[1], int(sys.argv[2]))
    